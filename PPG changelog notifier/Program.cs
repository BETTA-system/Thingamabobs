using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using OpenQA.Selenium;
using OpenQA.Selenium.Firefox;

class Program
{
    // Constants
    private const string ChangelogUrl = "https://raw.githubusercontent.com/studio-minus/people-playground-changelog/master/CHANGELOG.md";
    private const string DiscordWebhookUrl = "Webhook here";
    private const string LastContentFilePath = "lastContent.txt";

    static void Main()
    {
        // Firefox should not be visible
        var firefoxOptions = new FirefoxOptions();
        firefoxOptions.AddArguments("--headless");

        try
        {
            using (var driver = new FirefoxDriver(firefoxOptions))
            {
                driver.Navigate().GoToUrl(ChangelogUrl);

                // Check current changelog (online)
                var currentContent = driver.FindElement(By.TagName("body")).Text;

                // Check last changelog (local)
                var lastContent = File.Exists(LastContentFilePath) ? File.ReadAllText(LastContentFilePath) : string.Empty;

                // Compare for changes
                if (!currentContent.Equals(lastContent))
                {
                    var newContent = GetChangedContent(lastContent, currentContent);

                    // Update local file with current content
                    File.WriteAllText(LastContentFilePath, currentContent);

                    // Send new content to Discord
                    if (!string.IsNullOrEmpty(newContent))
                    {
                        SendToDiscord(DiscordWebhookUrl, newContent);
                        Console.WriteLine("Successfully sent to Discord");
                    }
                    else
                    {
                        Console.WriteLine("There is something wrong with change detection");
                    }
                }
                else
                {
                    Console.WriteLine("No changes detected");
                }
            }
        }
        catch (Exception ex)
        {
            // Print error to console for debugging
            Console.WriteLine("Error: " + ex.ToString());
        }
    }

    // Change detection logic
    private static string GetChangedContent(string oldContent, string newContent)
    {
        // List everything
        var oldLines = oldContent.Split('\n').ToList();
        var newLines = newContent.Split('\n').ToList();

        // Only additions 
        var addedLines = newLines.Except(oldLines).ToList();
        
        // Format for Discord
        var formattedContent = string.Join("\n", addedLines.Select(line => $"+ {line}"));

        return formattedContent;
    }

    // Send to Discord logic
    private static void SendToDiscord(string webhookUrl, string messageContent)
    {
        using (var client = new HttpClient())
        {
            // Format for Discord
            var message = $" Ping here \n```diff\n{messageContent}\n```";
            var payload = new { content = message };
            var jsonPayload = Newtonsoft.Json.JsonConvert.SerializeObject(payload);
            var data = new StringContent(jsonPayload, Encoding.UTF8, "application/json");

            // Send and check
            var response = client.PostAsync(webhookUrl, data).Result;
            if (!response.IsSuccessStatusCode)
            {
                throw new Exception("Failed to send message to Discord. Status code: " + response.StatusCode);
            }
        }
    }
}
// dotnet run
