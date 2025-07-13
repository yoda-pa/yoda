# Yoda v3 Makefile

# Variables
BINARY_NAME=yoda
BINARY_DIR=bin
CMD_DIR=cmd/yoda
VERSION?=3.0.0-dev
COMMIT=$(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
LDFLAGS=-ldflags "-X main.version=$(VERSION) -X main.commit=$(COMMIT)"

# Build targets
.PHONY: build clean test deps dev install uninstall help

## Build the binary
build:
	@echo "Building $(BINARY_NAME) v$(VERSION)..."
	@mkdir -p $(BINARY_DIR)
	go build $(LDFLAGS) -o $(BINARY_DIR)/$(BINARY_NAME) ./$(CMD_DIR)
	@echo "✅ Build complete: $(BINARY_DIR)/$(BINARY_NAME)"

## Build for development (with race detector)
dev:
	@echo "Building $(BINARY_NAME) for development..."
	@mkdir -p $(BINARY_DIR)
	go build -race $(LDFLAGS) -o $(BINARY_DIR)/$(BINARY_NAME)-dev ./$(CMD_DIR)
	@echo "✅ Development build complete: $(BINARY_DIR)/$(BINARY_NAME)-dev"

## Cross-platform builds
build-all: build-linux build-darwin build-windows
	@echo "✅ All platform builds complete"

build-linux:
	@echo "Building for Linux..."
	@mkdir -p $(BINARY_DIR)
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o $(BINARY_DIR)/$(BINARY_NAME)-linux-amd64 ./$(CMD_DIR)
	GOOS=linux GOARCH=arm64 go build $(LDFLAGS) -o $(BINARY_DIR)/$(BINARY_NAME)-linux-arm64 ./$(CMD_DIR)

build-darwin:
	@echo "Building for macOS..."
	@mkdir -p $(BINARY_DIR)
	GOOS=darwin GOARCH=amd64 go build $(LDFLAGS) -o $(BINARY_DIR)/$(BINARY_NAME)-darwin-amd64 ./$(CMD_DIR)
	GOOS=darwin GOARCH=arm64 go build $(LDFLAGS) -o $(BINARY_DIR)/$(BINARY_NAME)-darwin-arm64 ./$(CMD_DIR)

build-windows:
	@echo "Building for Windows..."
	@mkdir -p $(BINARY_DIR)
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o $(BINARY_DIR)/$(BINARY_NAME)-windows-amd64.exe ./$(CMD_DIR)

## Install dependencies
deps:
	@echo "Installing dependencies..."
	go mod download
	go mod tidy
	@echo "✅ Dependencies installed"

## Run tests
test:
	@echo "Running tests..."
	go test -v ./...
	@echo "✅ Tests complete"

## Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html
	@echo "✅ Coverage report generated: coverage.html"

## Run linter
lint:
	@echo "Running linter..."
	@which golangci-lint > /dev/null || (echo "Installing golangci-lint..." && go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest)
	golangci-lint run
	@echo "✅ Linting complete"

## Format code
fmt:
	@echo "Formatting code..."
	go fmt ./...
	@echo "✅ Code formatted"

## Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(BINARY_DIR)
	rm -f coverage.out coverage.html
	@echo "✅ Clean complete"

## Install binary to system
install: build
	@echo "Installing $(BINARY_NAME) to /usr/local/bin..."
	@sudo cp $(BINARY_DIR)/$(BINARY_NAME) /usr/local/bin/
	@echo "✅ $(BINARY_NAME) installed successfully"
	@echo "💡 Try running: yoda --help"

## Uninstall binary from system
uninstall:
	@echo "Uninstalling $(BINARY_NAME) from /usr/local/bin..."
	@sudo rm -f /usr/local/bin/$(BINARY_NAME)
	@echo "✅ $(BINARY_NAME) uninstalled successfully"

## Run the binary after building
run: build
	@echo "Running $(BINARY_NAME)..."
	./$(BINARY_DIR)/$(BINARY_NAME) $(ARGS)

## Initialize Yoda configuration
init: build
	@echo "Initializing Yoda configuration..."
	./$(BINARY_DIR)/$(BINARY_NAME) init

## Show available commands
help:
	@echo "Yoda v3 Build System"
	@echo ""
	@echo "Available commands:"
	@echo "  build         - Build the binary"
	@echo "  dev           - Build for development (with race detector)"
	@echo "  build-all     - Build for all platforms"
	@echo "  build-linux   - Build for Linux (amd64, arm64)"
	@echo "  build-darwin  - Build for macOS (amd64, arm64)"
	@echo "  build-windows - Build for Windows (amd64)"
	@echo "  deps          - Install dependencies"
	@echo "  test          - Run tests"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  lint          - Run linter"
	@echo "  fmt           - Format code"
	@echo "  clean         - Clean build artifacts"
	@echo "  install       - Install binary to system"
	@echo "  uninstall     - Uninstall binary from system"
	@echo "  run           - Build and run binary (use ARGS= for arguments)"
	@echo "  init          - Initialize Yoda configuration"
	@echo "  help          - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make build"
	@echo "  make run ARGS='--help'"
	@echo "  make install"
	@echo "  make test"