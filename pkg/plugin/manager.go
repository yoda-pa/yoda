package plugin

import (
	"fmt"
	"path/filepath"

	"github.com/94solutions/yoda/pkg/config"
	"github.com/94solutions/yoda/pkg/database"
	"github.com/spf13/cobra"
)

// Manager handles plugin management
type Manager struct {
	config   *config.Manager
	db       *database.Connection
	plugins  map[string]Plugin
	commands []*cobra.Command
}

// Plugin represents a Yoda plugin
type Plugin interface {
	Name() string
	Description() string
	Version() string
	Commands() []*cobra.Command
	Initialize() error
	Cleanup() error
	IsEnabled() bool
	SetEnabled(bool)
}

// BasePlugin provides a basic implementation of the Plugin interface
type BasePlugin struct {
	name        string
	description string
	version     string
	enabled     bool
}

// NewManager creates a new plugin manager
func NewManager(configManager *config.Manager) *Manager {
	return &Manager{
		config:   configManager,
		plugins:  make(map[string]Plugin),
		commands: make([]*cobra.Command, 0),
	}
}

// LoadPlugins discovers and loads all available plugins
func (m *Manager) LoadPlugins() error {
	// Initialize database connection if not already done
	if m.db == nil {
		dbPath := filepath.Join(m.config.GetConfigDir(), "yoda.db")
		db, err := database.Connect(dbPath)
		if err != nil {
			return fmt.Errorf("failed to connect to database: %w", err)
		}
		m.db = db

		// Initialize plugin tables
		if err := m.initPluginTables(); err != nil {
			return fmt.Errorf("failed to initialize plugin tables: %w", err)
		}
	}

	// Load built-in plugins
	if err := m.loadBuiltinPlugins(); err != nil {
		return fmt.Errorf("failed to load builtin plugins: %w", err)
	}

	// Load external plugins (future implementation)
	// TODO: Implement external plugin loading

	return nil
}

// initPluginTables creates the necessary database tables for plugin management
func (m *Manager) initPluginTables() error {
	queries := []string{
		`CREATE TABLE IF NOT EXISTS plugins (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT UNIQUE NOT NULL,
			version TEXT NOT NULL,
			enabled BOOLEAN DEFAULT TRUE,
			config_path TEXT,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE TABLE IF NOT EXISTS plugin_configs (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			plugin_id INTEGER NOT NULL,
			key TEXT NOT NULL,
			value TEXT NOT NULL,
			FOREIGN KEY(plugin_id) REFERENCES plugins(id),
			UNIQUE(plugin_id, key)
		)`,
	}

	for _, query := range queries {
		if _, err := m.db.Exec(query); err != nil {
			return fmt.Errorf("failed to execute query: %w", err)
		}
	}

	return nil
}

// loadBuiltinPlugins loads the built-in plugins
func (m *Manager) loadBuiltinPlugins() error {
	// Register built-in plugins here
	// For now, we'll just register them in the database
	builtinPlugins := []struct {
		name        string
		version     string
		description string
	}{
		{"config", "1.0.0", "Configuration management plugin"},
		{"plugin", "1.0.0", "Plugin management plugin"},
	}

	for _, p := range builtinPlugins {
		if err := m.registerPlugin(p.name, p.version, true); err != nil {
			return fmt.Errorf("failed to register plugin %s: %w", p.name, err)
		}
	}

	return nil
}

// registerPlugin registers a plugin in the database
func (m *Manager) registerPlugin(name, version string, enabled bool) error {
	query := `INSERT OR REPLACE INTO plugins (name, version, enabled, updated_at) 
			  VALUES (?, ?, ?, CURRENT_TIMESTAMP)`
	
	_, err := m.db.Exec(query, name, version, enabled)
	return err
}

// GetPlugins returns all loaded plugins
func (m *Manager) GetPlugins() map[string]Plugin {
	return m.plugins
}

// GetPlugin returns a specific plugin by name
func (m *Manager) GetPlugin(name string) (Plugin, bool) {
	plugin, exists := m.plugins[name]
	return plugin, exists
}

// GetCommands returns all plugin commands
func (m *Manager) GetCommands() []*cobra.Command {
	return m.commands
}

// EnablePlugin enables a plugin
func (m *Manager) EnablePlugin(name string) error {
	query := `UPDATE plugins SET enabled = TRUE, updated_at = CURRENT_TIMESTAMP WHERE name = ?`
	result, err := m.db.Exec(query, name)
	if err != nil {
		return fmt.Errorf("failed to enable plugin: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get affected rows: %w", err)
	}

	if rowsAffected == 0 {
		return fmt.Errorf("plugin %s not found", name)
	}

	// Update plugin object if loaded
	if plugin, exists := m.plugins[name]; exists {
		plugin.SetEnabled(true)
	}

	return nil
}

// DisablePlugin disables a plugin
func (m *Manager) DisablePlugin(name string) error {
	// Prevent disabling protected plugins
	protectedPlugins := []string{"config", "plugin"}
	for _, protected := range protectedPlugins {
		if name == protected {
			return fmt.Errorf("plugin %s is protected and cannot be disabled", name)
		}
	}

	query := `UPDATE plugins SET enabled = FALSE, updated_at = CURRENT_TIMESTAMP WHERE name = ?`
	result, err := m.db.Exec(query, name)
	if err != nil {
		return fmt.Errorf("failed to disable plugin: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get affected rows: %w", err)
	}

	if rowsAffected == 0 {
		return fmt.Errorf("plugin %s not found", name)
	}

	// Update plugin object if loaded
	if plugin, exists := m.plugins[name]; exists {
		plugin.SetEnabled(false)
	}

	return nil
}

// ListPlugins returns information about all plugins
func (m *Manager) ListPlugins() ([]PluginInfo, error) {
	query := `SELECT name, version, enabled FROM plugins ORDER BY name`
	rows, err := m.db.Query(query)
	if err != nil {
		return nil, fmt.Errorf("failed to query plugins: %w", err)
	}
	defer rows.Close()

	var plugins []PluginInfo
	for rows.Next() {
		var info PluginInfo
		if err := rows.Scan(&info.Name, &info.Version, &info.Enabled); err != nil {
			return nil, fmt.Errorf("failed to scan plugin row: %w", err)
		}
		plugins = append(plugins, info)
	}

	return plugins, nil
}

// PluginInfo contains basic information about a plugin
type PluginInfo struct {
	Name        string `json:"name"`
	Version     string `json:"version"`
	Enabled     bool   `json:"enabled"`
	Description string `json:"description,omitempty"`
}

// RefreshPlugins re-discovers and reloads all plugins
func (m *Manager) RefreshPlugins() error {
	// Clear current plugins
	m.plugins = make(map[string]Plugin)
	m.commands = make([]*cobra.Command, 0)

	// Reload plugins
	return m.LoadPlugins()
}

// Cleanup cleans up plugin manager resources
func (m *Manager) Cleanup() error {
	// Cleanup all loaded plugins
	for _, plugin := range m.plugins {
		if err := plugin.Cleanup(); err != nil {
			// Log error but continue cleanup
			fmt.Printf("Warning: Failed to cleanup plugin %s: %v\n", plugin.Name(), err)
		}
	}

	// Close database connection
	if m.db != nil {
		return m.db.Close()
	}

	return nil
}

// BasePlugin implementation

// NewBasePlugin creates a new base plugin
func NewBasePlugin(name, description, version string) *BasePlugin {
	return &BasePlugin{
		name:        name,
		description: description,
		version:     version,
		enabled:     true,
	}
}

// Name returns the plugin name
func (p *BasePlugin) Name() string {
	return p.name
}

// Description returns the plugin description
func (p *BasePlugin) Description() string {
	return p.description
}

// Version returns the plugin version
func (p *BasePlugin) Version() string {
	return p.version
}

// Commands returns the plugin commands (empty for base plugin)
func (p *BasePlugin) Commands() []*cobra.Command {
	return []*cobra.Command{}
}

// Initialize initializes the plugin (no-op for base plugin)
func (p *BasePlugin) Initialize() error {
	return nil
}

// Cleanup cleans up the plugin (no-op for base plugin)
func (p *BasePlugin) Cleanup() error {
	return nil
}

// IsEnabled returns whether the plugin is enabled
func (p *BasePlugin) IsEnabled() bool {
	return p.enabled
}

// SetEnabled sets the plugin enabled state
func (p *BasePlugin) SetEnabled(enabled bool) {
	p.enabled = enabled
}