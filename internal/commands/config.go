package commands

import (
	"fmt"
	"os"

	"github.com/94solutions/yoda/pkg/config"
	"github.com/spf13/cobra"
)

// NewConfigCommand creates the config command
func NewConfigCommand(configManager *config.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "config",
		Short: "Configuration management",
		Long:  `Manage Yoda configuration settings. View, set, and modify configuration values.`,
	}

	// Add subcommands
	cmd.AddCommand(newConfigGetCommand(configManager))
	cmd.AddCommand(newConfigSetCommand(configManager))
	cmd.AddCommand(newConfigListCommand(configManager))
	cmd.AddCommand(newConfigEditCommand(configManager))

	return cmd
}

func newConfigGetCommand(configManager *config.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "get <key>",
		Short: "Get a configuration value",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := configManager.Load(); err != nil {
				return fmt.Errorf("failed to load configuration: %w", err)
			}

			key := args[0]
			value := configManager.Get(key)
			
			if value == nil {
				fmt.Printf("Configuration key '%s' not found\n", key)
				return nil
			}

			fmt.Printf("%s = %v\n", key, value)
			return nil
		},
	}

	return cmd
}

func newConfigSetCommand(configManager *config.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "set <key> <value>",
		Short: "Set a configuration value",
		Args:  cobra.ExactArgs(2),
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := configManager.Load(); err != nil {
				return fmt.Errorf("failed to load configuration: %w", err)
			}

			key := args[0]
			value := args[1]

			configManager.Set(key, value)

			if err := configManager.Save(); err != nil {
				return fmt.Errorf("failed to save configuration: %w", err)
			}

			fmt.Printf("✅ Set %s = %s\n", key, value)
			return nil
		},
	}

	return cmd
}

func newConfigListCommand(configManager *config.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "list",
		Short: "List all configuration values",
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := configManager.Load(); err != nil {
				return fmt.Errorf("failed to load configuration: %w", err)
			}

			config, err := configManager.GetConfig()
			if err != nil {
				return fmt.Errorf("failed to get configuration: %w", err)
			}

			fmt.Println("📋 Current Configuration:")
			fmt.Println()

			// Global AI settings
			fmt.Println("🤖 AI Settings:")
			fmt.Printf("  Model: %s\n", config.Global.AI.Model)
			fmt.Printf("  Max Context Length: %d\n", config.Global.AI.MaxContextLength)
			fmt.Printf("  Temperature: %.1f\n", config.Global.AI.Temperature)
			fmt.Printf("  Base URL: %s\n", config.Global.AI.BaseURL)
			fmt.Println()

			// Global Plugin settings
			fmt.Println("🔌 Plugin Settings:")
			fmt.Printf("  Auto Discovery: %v\n", config.Global.Plugins.AutoDiscovery)
			fmt.Printf("  Trusted Sources: %v\n", config.Global.Plugins.TrustedSources)
			fmt.Printf("  Plugin Directories: %v\n", config.Global.Plugins.PluginDirs)
			fmt.Printf("  Disabled Plugins: %v\n", config.Global.Plugins.DisabledPlugins)
			fmt.Println()

			// Security settings
			fmt.Println("🔒 Security Settings:")
			fmt.Printf("  Plugin Sandboxing: %v\n", config.Global.Security.PluginSandboxing)
			fmt.Printf("  API Rate Limiting: %v\n", config.Global.Security.APIRateLimiting)

			if len(config.Plugins) > 0 {
				fmt.Println()
				fmt.Println("🔧 Plugin-specific Settings:")
				for name, pluginConfig := range config.Plugins {
					fmt.Printf("  %s:\n", name)
					fmt.Printf("    Enabled: %v\n", pluginConfig.Enabled)
					if len(pluginConfig.Config) > 0 {
						for key, value := range pluginConfig.Config {
							fmt.Printf("    %s: %v\n", key, value)
						}
					}
				}
			}

			return nil
		},
	}

	return cmd
}

func newConfigEditCommand(configManager *config.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "edit",
		Short: "Edit configuration file with default editor",
		RunE: func(cmd *cobra.Command, args []string) error {
			configFile := configManager.GetConfigFile()
			
			// Get editor from environment or use default
			editor := os.Getenv("EDITOR")
			if editor == "" {
				editor = "nano" // Default to nano on Unix-like systems
				if os.Getenv("OS") == "Windows_NT" {
					editor = "notepad"
				}
			}

			fmt.Printf("Opening %s with %s...\n", configFile, editor)
			
			// For now, just show the file path
			// TODO: Implement actual editor opening
			fmt.Printf("Please edit the configuration file at: %s\n", configFile)
			
			return nil
		},
	}

	return cmd
}