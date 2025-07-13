package commands

import (
	"fmt"

	"github.com/94solutions/yoda/pkg/config"
	"github.com/spf13/cobra"
)

// NewInitCommand creates the init command
func NewInitCommand(configManager *config.Manager) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "init",
		Short: "Initialize Yoda configuration",
		Long:  `Initialize Yoda configuration files and directories. This command sets up the necessary configuration structure for Yoda to work properly.`,
		RunE: func(cmd *cobra.Command, args []string) error {
			return runInit(configManager)
		},
	}

	return cmd
}

func runInit(configManager *config.Manager) error {
	fmt.Println("Initializing Yoda configuration...")

	// Initialize configuration
	if err := configManager.Initialize(); err != nil {
		return fmt.Errorf("failed to initialize configuration: %w", err)
	}

	// Load the configuration to ensure it's valid
	if err := configManager.Load(); err != nil {
		return fmt.Errorf("failed to load configuration: %w", err)
	}

	fmt.Printf("✅ Configuration initialized successfully!\n")
	fmt.Printf("📁 Configuration directory: %s\n", configManager.GetConfigDir())
	fmt.Printf("📄 Configuration file: %s\n", configManager.GetConfigFile())
	
	fmt.Println("\n🚀 Yoda is ready to use! Try running:")
	fmt.Println("   yoda --help")
	fmt.Println("   yoda plugin list")

	return nil
}