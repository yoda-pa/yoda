package commands

import (
	"fmt"
	"os"
	"text/tabwriter"

	"github.com/94solutions/yoda/pkg/plugin"
	"github.com/spf13/cobra"
)

// NewPluginCommand creates the plugin command
func NewPluginCommand(pluginManager *plugin.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "plugin",
		Short: "Plugin management",
		Long:  `Manage Yoda plugins. List, enable, disable, and refresh plugins.`,
	}

	// Add subcommands
	cmd.AddCommand(newPluginListCommand(pluginManager))
	cmd.AddCommand(newPluginEnableCommand(pluginManager))
	cmd.AddCommand(newPluginDisableCommand(pluginManager))
	cmd.AddCommand(newPluginRefreshCommand(pluginManager))

	return cmd
}

func newPluginListCommand(pluginManager *plugin.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "list",
		Short: "List all available plugins",
		RunE: func(cmd *cobra.Command, args []string) error {
			plugins, err := pluginManager.ListPlugins()
			if err != nil {
				return fmt.Errorf("failed to list plugins: %w", err)
			}

			if len(plugins) == 0 {
				fmt.Println("📦 No plugins found.")
				fmt.Println("💡 Try running 'yoda plugin refresh' to discover plugins.")
				return nil
			}

			fmt.Println("📦 Available Plugins:")
			fmt.Println()

			// Create a tab writer for aligned output
			w := tabwriter.NewWriter(os.Stdout, 0, 0, 3, ' ', 0)
			fmt.Fprintln(w, "NAME\tVERSION\tSTATUS")
			fmt.Fprintln(w, "----\t-------\t------")

			for _, p := range plugins {
				status := "❌ Disabled"
				if p.Enabled {
					status = "✅ Enabled"
				}
				fmt.Fprintf(w, "%s\t%s\t%s\n", p.Name, p.Version, status)
			}

			w.Flush()
			return nil
		},
	}

	return cmd
}

func newPluginEnableCommand(pluginManager *plugin.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "enable <plugin-name>",
		Short: "Enable a plugin",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			pluginName := args[0]

			if err := pluginManager.EnablePlugin(pluginName); err != nil {
				return fmt.Errorf("failed to enable plugin '%s': %w", pluginName, err)
			}

			fmt.Printf("✅ Plugin '%s' enabled successfully\n", pluginName)
			fmt.Println("💡 You may need to restart Yoda for changes to take effect.")
			return nil
		},
	}

	return cmd
}

func newPluginDisableCommand(pluginManager *plugin.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "disable <plugin-name>",
		Short: "Disable a plugin",
		Args:  cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			pluginName := args[0]

			if err := pluginManager.DisablePlugin(pluginName); err != nil {
				return fmt.Errorf("failed to disable plugin '%s': %w", pluginName, err)
			}

			fmt.Printf("❌ Plugin '%s' disabled successfully\n", pluginName)
			fmt.Println("💡 You may need to restart Yoda for changes to take effect.")
			return nil
		},
	}

	return cmd
}

func newPluginRefreshCommand(pluginManager *plugin.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "refresh",
		Short: "Refresh and rediscover plugins",
		Long:  `Re-discover all available plugins and reload the plugin registry. This command scans for new plugins and updates the plugin database.`,
		RunE: func(cmd *cobra.Command, args []string) error {
			fmt.Println("🔄 Refreshing plugins...")

			if err := pluginManager.RefreshPlugins(); err != nil {
				return fmt.Errorf("failed to refresh plugins: %w", err)
			}

			plugins, err := pluginManager.ListPlugins()
			if err != nil {
				return fmt.Errorf("failed to list plugins after refresh: %w", err)
			}

			fmt.Printf("✅ Plugin refresh completed! Found %d plugins.\n", len(plugins))
			
			if len(plugins) > 0 {
				fmt.Println("💡 Run 'yoda plugin list' to see all available plugins.")
			}

			return nil
		},
	}

	return cmd
}