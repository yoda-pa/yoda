package config

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/spf13/viper"
)

// Manager handles configuration management for Yoda
type Manager struct {
	configDir  string
	configFile string
	v          *viper.Viper
}

// Config represents the application configuration
type Config struct {
	Global  GlobalConfig            `mapstructure:"global"`
	Plugins map[string]PluginConfig `mapstructure:"plugins"`
}

// GlobalConfig contains global application settings
type GlobalConfig struct {
	AI       AIConfig       `mapstructure:"ai"`
	Plugins  PluginsConfig  `mapstructure:"plugins"`
	Security SecurityConfig `mapstructure:"security"`
}

// AIConfig contains AI-related settings
type AIConfig struct {
	Model            string  `mapstructure:"model"`
	MaxContextLength int     `mapstructure:"max_context_length"`
	Temperature      float64 `mapstructure:"temperature"`
	BaseURL          string  `mapstructure:"base_url"`
}

// PluginsConfig contains plugin-related settings
type PluginsConfig struct {
	AutoDiscovery   bool     `mapstructure:"auto_discovery"`
	TrustedSources  []string `mapstructure:"trusted_sources"`
	PluginDirs      []string `mapstructure:"plugin_dirs"`
	DisabledPlugins []string `mapstructure:"disabled_plugins"`
}

// SecurityConfig contains security settings
type SecurityConfig struct {
	PluginSandboxing bool `mapstructure:"plugin_sandboxing"`
	APIRateLimiting  bool `mapstructure:"api_rate_limiting"`
}

// PluginConfig represents individual plugin configuration
type PluginConfig struct {
	Enabled bool                   `mapstructure:"enabled"`
	Config  map[string]interface{} `mapstructure:"config"`
}

// NewManager creates a new configuration manager
func NewManager() *Manager {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		homeDir = "."
	}

	configDir := filepath.Join(homeDir, ".yoda")
	
	v := viper.New()
	v.SetConfigName("config")
	v.SetConfigType("yaml")
	v.AddConfigPath(configDir)

	// Set defaults
	setDefaults(v)

	return &Manager{
		configDir:  configDir,
		configFile: filepath.Join(configDir, "config.yaml"),
		v:          v,
	}
}

// setDefaults sets default configuration values
func setDefaults(v *viper.Viper) {
	// AI defaults
	v.SetDefault("global.ai.model", "codellama")
	v.SetDefault("global.ai.max_context_length", 4096)
	v.SetDefault("global.ai.temperature", 0.7)
	v.SetDefault("global.ai.base_url", "http://localhost:11434")

	// Plugin defaults
	v.SetDefault("global.plugins.auto_discovery", true)
	v.SetDefault("global.plugins.trusted_sources", []string{"official", "community"})
	v.SetDefault("global.plugins.plugin_dirs", []string{})
	v.SetDefault("global.plugins.disabled_plugins", []string{})

	// Security defaults
	v.SetDefault("global.security.plugin_sandboxing", true)
	v.SetDefault("global.security.api_rate_limiting", true)
}

// Initialize creates the configuration directory and file if they don't exist
func (m *Manager) Initialize() error {
	// Create config directory
	if err := os.MkdirAll(m.configDir, 0755); err != nil {
		return fmt.Errorf("failed to create config directory: %w", err)
	}

	// Check if config file exists
	if _, err := os.Stat(m.configFile); os.IsNotExist(err) {
		// Create default config file
		if err := m.v.SafeWriteConfigAs(m.configFile); err != nil {
			return fmt.Errorf("failed to create config file: %w", err)
		}
	}

	return nil
}

// Load reads the configuration from file
func (m *Manager) Load() error {
	if err := m.v.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			// Config file not found, use defaults
			return nil
		}
		return fmt.Errorf("failed to read config file: %w", err)
	}
	return nil
}

// Save writes the current configuration to file
func (m *Manager) Save() error {
	return m.v.WriteConfig()
}

// Get retrieves a configuration value
func (m *Manager) Get(key string) interface{} {
	return m.v.Get(key)
}

// GetString retrieves a string configuration value
func (m *Manager) GetString(key string) string {
	return m.v.GetString(key)
}

// GetBool retrieves a boolean configuration value
func (m *Manager) GetBool(key string) bool {
	return m.v.GetBool(key)
}

// GetInt retrieves an integer configuration value
func (m *Manager) GetInt(key string) int {
	return m.v.GetInt(key)
}

// GetFloat64 retrieves a float64 configuration value
func (m *Manager) GetFloat64(key string) float64 {
	return m.v.GetFloat64(key)
}

// GetStringSlice retrieves a string slice configuration value
func (m *Manager) GetStringSlice(key string) []string {
	return m.v.GetStringSlice(key)
}

// Set sets a configuration value
func (m *Manager) Set(key string, value interface{}) {
	m.v.Set(key, value)
}

// GetConfig returns the full configuration struct
func (m *Manager) GetConfig() (*Config, error) {
	var config Config
	if err := m.v.Unmarshal(&config); err != nil {
		return nil, fmt.Errorf("failed to unmarshal config: %w", err)
	}
	return &config, nil
}

// GetConfigDir returns the configuration directory path
func (m *Manager) GetConfigDir() string {
	return m.configDir
}

// GetConfigFile returns the configuration file path
func (m *Manager) GetConfigFile() string {
	return m.configFile
}