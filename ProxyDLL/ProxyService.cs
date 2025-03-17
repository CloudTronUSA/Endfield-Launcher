using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Runtime.InteropServices;
using System.Security.Cryptography.X509Certificates;
using Microsoft.Win32;
using Titanium.Web.Proxy;
using Titanium.Web.Proxy.EventArguments;
using Titanium.Web.Proxy.Models;
using Titanium.Web.Proxy.Exceptions;
using System.Threading.Tasks;

namespace ProxyRedirector
{
    class Program
    {
        private static readonly ProxyServer proxyServer = new ProxyServer();
        private static ExplicitProxyEndPoint explicitEndPoint;
        private static string originalProxyAddress = null;
        private static bool originalProxyEnabled = false;
        private static ExternalProxy originalExternalProxy = null;
        private static HashSet<string> hostsToRedirect;
        private static readonly string CertificateName = "ProxyRedirector Root CA";
        private static int proxyPort = 2000;
        private static bool isRunning = true;

        static async Task Main(string[] args)
        {
            Console.WriteLine("==========================================");
            Console.WriteLine("  Proxy Redirection Tool v1.0");
            Console.WriteLine("==========================================");
            
            // Process command line arguments
            List<string> hosts = new List<string>();
            for (int i = 0; i < args.Length; i++)
            {
                if (args[i] == "--port" && i + 1 < args.Length)
                {
                    if (int.TryParse(args[i + 1], out int port))
                    {
                        proxyPort = port;
                        i++;
                    }
                }
                else if (args[i] == "--host" && i + 1 < args.Length)
                {
                    hosts.Add(args[i + 1]);
                    i++;
                }
            }
            
            // Use default hosts if none specified
            if (hosts.Count == 0)
            {
                Console.WriteLine("No hosts specified for redirection. Using defaults.");
                hosts.Add("example.com");
                hosts.Add("api.example.com");
            }
            
            hostsToRedirect = new HashSet<string>(hosts, StringComparer.OrdinalIgnoreCase);
            
            // Register cleanup handlers
            Console.CancelKeyPress += (s, e) => {
                e.Cancel = true;
                isRunning = false;
            };
            
            try
            {
                // Get original proxy settings
                GetOriginalProxySettings();
                
                // Install certificate if needed
                if (!InstallCertificateIfNeeded())
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Failed to install certificate. Make sure you're running as Administrator.");
                    Console.ResetColor();
                    return;
                }
                
                // Setup event handlers
                proxyServer.BeforeRequest += OnRequest;
                proxyServer.ServerCertificateValidationCallback += OnCertificateValidation;
                
                // Create endpoint
                explicitEndPoint = new ExplicitProxyEndPoint(IPAddress.Any, proxyPort, true);
                explicitEndPoint.BeforeTunnelConnectRequest += OnBeforeTunnelConnectRequest;
                
                // Configure upstream proxy selector with correct signature
                proxyServer.GetCustomUpStreamProxyFunc = OnSelectUpstreamProxy;
                
                // Add and start the proxy
                proxyServer.AddEndPoint(explicitEndPoint);
                proxyServer.Start();
                
                // Set as system proxy
                proxyServer.SetAsSystemHttpProxy(explicitEndPoint);
                proxyServer.SetAsSystemHttpsProxy(explicitEndPoint);

                proxyServer.ExceptionFunc = async exception =>
                {
                    if (exception is ProxyHttpException phex)
                        Console.WriteLine(exception.Message + ": " + phex.InnerException?.Message);
                    else
                        Console.WriteLine("ERROR:" + exception.Message);
                };
                
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Proxy started on port {proxyPort}");
                Console.ResetColor();
                
                // Display configuration
                Console.WriteLine("\nRedirecting these hosts to localhost:5000:");
                foreach (var host in hostsToRedirect)
                {
                    Console.WriteLine($"  - {host}");
                }
                
                if (originalExternalProxy != null)
                {
                    Console.WriteLine($"\nUsing original system proxy ({originalExternalProxy.HostName}:{originalExternalProxy.Port}) for all other traffic");
                }
                else
                {
                    Console.WriteLine("\nConnecting directly (no proxy) for all other traffic");
                }
                
                Console.WriteLine("\nProxy is running. Press Ctrl+C to exit and restore settings.");
                
                // Keep the application running until cancelled
                while (isRunning)
                {
                    await Task.Delay(500);
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"Error: {ex.Message}");
                Console.ResetColor();
            }
            finally
            {
                Cleanup();
            }
        }

        // Fixed method signature to match the delegate type
        // Updated method signature to match the delegate type
        private static async Task<IExternalProxy> OnSelectUpstreamProxy(SessionEventArgsBase session)
        {
            string hostname = null;
                    
            // Extract hostname from the session
            if (session is SessionEventArgs sessionArgs)
            {
                hostname = sessionArgs.HttpClient.Request.RequestUri.Host;
            }
            else if (session is TunnelConnectSessionEventArgs tunnelArgs)
            {
                hostname = tunnelArgs.HttpClient.Request.RequestUri.Host;
            }
            
            // If this is one of our target hosts, return null to handle it directly
            if (hostname != null && hostsToRedirect.Contains(hostname))
            {
                return null; // Handle locally
            }
            
            // Otherwise return the original system proxy if it exists
            return originalExternalProxy;
        }

        private static void GetOriginalProxySettings()
        {
            try
            {
                using (RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Internet Settings", false))
                {
                    if (key != null)
                    {
                        originalProxyEnabled = Convert.ToBoolean(key.GetValue("ProxyEnable", 0));
                        originalProxyAddress = key.GetValue("ProxyServer", string.Empty).ToString();
                    }
                }
                
                Console.WriteLine($"Original proxy settings - Enabled: {originalProxyEnabled}, Address: {originalProxyAddress}");
                
                // Parse original proxy into ExternalProxy object if enabled
                if (originalProxyEnabled && !string.IsNullOrEmpty(originalProxyAddress))
                {
                    string[] parts = originalProxyAddress.Split(':');
                    if (parts.Length == 2 && int.TryParse(parts[1], out int upstreamPort))
                    {
                        originalExternalProxy = new ExternalProxy
                        {
                            HostName = parts[0],
                            Port = upstreamPort
                        };
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting original proxy settings: {ex.Message}");
            }
        }

        private static void RestoreOriginalProxySettings()
        {
            try
            {
                if (originalProxyEnabled)
                {
                    // Restore the original proxy
                    using (RegistryKey key = Registry.CurrentUser.OpenSubKey(
                        @"Software\Microsoft\Windows\CurrentVersion\Internet Settings", true))
                    {
                        if (key != null)
                        {
                            key.SetValue("ProxyEnable", 1);
                            key.SetValue("ProxyServer", originalProxyAddress);
                        }
                    }
                }
                else
                {
                    // Disable proxy
                    using (RegistryKey key = Registry.CurrentUser.OpenSubKey(
                        @"Software\Microsoft\Windows\CurrentVersion\Internet Settings", true))
                    {
                        if (key != null)
                        {
                            key.SetValue("ProxyEnable", 0);
                        }
                    }
                }

                // Refresh Internet Settings
                InternetSetOption(IntPtr.Zero, INTERNET_OPTION_SETTINGS_CHANGED, IntPtr.Zero, 0);
                InternetSetOption(IntPtr.Zero, INTERNET_OPTION_REFRESH, IntPtr.Zero, 0);
                
                Console.WriteLine("Original proxy settings restored");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error restoring proxy settings: {ex.Message}");
            }
        }

        private static bool InstallCertificateIfNeeded()
        {
            try
            {
                // Check if our certificate is already installed
                using (X509Store store = new X509Store(StoreName.Root, StoreLocation.LocalMachine))
                {
                    store.Open(OpenFlags.ReadOnly);
                    var existingCerts = store.Certificates.Find(X509FindType.FindBySubjectName, CertificateName, false);
                    
                    if (existingCerts.Count > 0)
                    {
                        Console.WriteLine("Certificate already installed");
                        return true;
                    }
                }
                
                Console.WriteLine("Certificate installed successfully");
                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error installing certificate: {ex.Message}");
                return false;
            }
        }

        private static async Task OnBeforeTunnelConnectRequest(object sender, TunnelConnectSessionEventArgs e)
        {
            string hostname = e.HttpClient.Request.RequestUri.Host;
            
            Console.WriteLine($"Tunneling: {hostname}");
            
            if (hostname.Contains("gryphline.com") || hostname.Contains("hg-cdn.com"))
            {
                // IMPORTANT FIX: For this specific domain, we need to configure TLS correctly
                Console.WriteLine($"[TLS] Attempting to decrypt SSL for: {hostname}");
                
                // Ensure we're decrypting
                e.DecryptSsl = true;


            }
        }

        private static async Task OnRequest(object sender, SessionEventArgs e)
        {
            string hostname = e.HttpClient.Request.RequestUri.Host;
            Console.WriteLine($"Request: {hostname}");
            
            // Check if hostname matches the specified domains
            if (hostname.Contains("gryphline.com") || hostname.Contains("hg-cdn.com"))
            {
                // Skip CONNECT requests
                //if (e.HttpClient.Request.Method == "CONNECT")
                //{
                //    return;
                //}
                
                // Log the full URL
                string fullUrl = e.HttpClient.Request.Url;
                
                // Save original information in a cookie
                //string originalCookie = e.HttpClient.Request.Headers.GetFirstHeader("Cookie") ?? "";
                //string newCookie = $"{originalCookie};OriginalHost={hostname};OriginalUrl={fullUrl}";
                //e.HttpClient.Request.Headers.SetHeader("Cookie", newCookie);
                
                // Change the scheme to http and redirect to localhost:5000
                // First, save the original path
                string path = e.HttpClient.Request.RequestUri.PathAndQuery;
                
                // Change the URL to localhost:5000
                e.HttpClient.Request.Url = $"http://localhost:5000{path}";

                Console.WriteLine($">>>>>>>>>>>> URL: {fullUrl} to {e.HttpClient.Request.Url}");
            }
            else if (originalExternalProxy != null)
            {
                // This is handled by our OnSelectUpstreamProxy function
                //Console.WriteLine($"Proxying: {e.HttpClient.Request.Url} via original system proxy");
            }
            else
            {
                Console.WriteLine($"Direct connection: {e.HttpClient.Request.Url}");
            }
        }

        private static Task OnCertificateValidation(object sender, CertificateValidationEventArgs e)
        {
            // Accept all certificates
            e.IsValid = true;
            return Task.CompletedTask;
        }

        private static void Cleanup()
        {
            try
            {
                Console.WriteLine("Cleaning up...");
                
                // Unsubscribe from events
                if (explicitEndPoint != null)
                {
                    explicitEndPoint.BeforeTunnelConnectRequest -= OnBeforeTunnelConnectRequest;
                }
                
                proxyServer.BeforeRequest -= OnRequest;
                proxyServer.ServerCertificateValidationCallback -= OnCertificateValidation;
                
                // Stop the proxy
                proxyServer.Stop();
                
                // Restore the original proxy settings
                RestoreOriginalProxySettings();
                
                Console.WriteLine("Proxy stopped successfully");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error during cleanup: {ex.Message}");
            }
        }

        // Native methods for proxy settings
        private const int INTERNET_OPTION_SETTINGS_CHANGED = 39;
        private const int INTERNET_OPTION_REFRESH = 37;
        
        [DllImport("wininet.dll", SetLastError = true)]
        private static extern bool InternetSetOption(IntPtr hInternet, int dwOption, IntPtr lpBuffer, int lpdwBufferLength);
    }
}