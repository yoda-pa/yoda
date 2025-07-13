package main

import (
	"fmt"
	"os"

	"github.com/94solutions/yoda/internal/commands"
	"github.com/94solutions/yoda/pkg/config"
	"github.com/94solutions/yoda/pkg/plugin"
	"github.com/spf13/cobra"
)

var (
	version = "3.0.0"
	commit  = "dev"
)

func main() {
	configManager := config.NewManager()
	pluginManager := plugin.NewManager(configManager)

	rootCmd := &cobra.Command{
		Use:     "yoda",
		Short:   "Personal Assistant on the command line",
		Long:    "Yoda is an extensible CLI personal assistant with AI capabilities and plugin support.",
		Version: fmt.Sprintf("%s (%s)", version, commit),
	}

	// Add core commands
	rootCmd.AddCommand(commands.NewInitCommand(configManager))
	rootCmd.AddCommand(commands.NewConfigCommand(configManager))
	rootCmd.AddCommand(commands.NewPluginCommand(pluginManager))

	// Load and add plugin commands
	if err := pluginManager.LoadPlugins(); err != nil {
		fmt.Fprintf(os.Stderr, "Warning: Error loading plugins: %v\n", err)
	}

	pluginCommands := pluginManager.GetCommands()
	for _, cmd := range pluginCommands {
		rootCmd.AddCommand(cmd)
	}

	// Execute the command
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}