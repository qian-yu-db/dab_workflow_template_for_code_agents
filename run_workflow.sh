#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${BLUE}INFO: $1${NC}"
}

print_success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# Default values
PROFILE=""
TARGET="dev"
SKIP_VALIDATION=false
SKIP_DEPLOYMENT=false
JOB_ID=""
VAR_OVERRIDES=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --profile)
            PROFILE="$2"
            shift 2
            ;;
        --target)
            TARGET="$2"
            shift 2
            ;;
        --skip-validation)
            SKIP_VALIDATION=true
            shift
            ;;
        --skip-deployment)
            SKIP_DEPLOYMENT=true
            shift
            ;;
        --job-id)
            JOB_ID="$2"
            shift 2
            ;;
        --var)
            VAR_OVERRIDES+=("--var" "$2")
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Set profile flag if provided
PROFILE_FLAG=""
if [ -n "$PROFILE" ]; then
    PROFILE_FLAG="--profile $PROFILE"
    print_info "Using Databricks profile: $PROFILE"
fi

# Validate bundle
if [ "$SKIP_VALIDATION" = false ]; then
    print_info "Validating Databricks Asset Bundle..."
    if databricks bundle validate $PROFILE_FLAG -t $TARGET; then
        print_success "Bundle validation passed"
    else
        print_error "Bundle validation failed"
        exit 1
    fi
fi

# Deploy bundle
if [ "$SKIP_DEPLOYMENT" = false ] && [ -z "$JOB_ID" ]; then
    print_info "Deploying bundle to $TARGET environment..."
    if databricks bundle deploy $PROFILE_FLAG -t $TARGET "${VAR_OVERRIDES[@]}"; then
        print_success "Bundle deployed successfully"
    else
        print_error "Bundle deployment failed"
        exit 1
    fi
fi

# Run job
if [ -n "$JOB_ID" ]; then
    print_info "Running existing job ID: $JOB_ID"
    RUN_OUTPUT=$(databricks jobs run-now $PROFILE_FLAG --job-id $JOB_ID)
else
    print_info "Running job: document_processing_pipeline_job"
    RUN_OUTPUT=$(databricks bundle run $PROFILE_FLAG document_processing_pipeline_job -t $TARGET)
fi

# Extract run ID
RUN_ID=$(echo "$RUN_OUTPUT" | grep -oP 'run_id=\K[0-9]+' || echo "")

if [ -n "$RUN_ID" ]; then
    print_success "Job started with run ID: $RUN_ID"
    print_info "Monitor at: https://e2-demo-field-eng.cloud.databricks.com/#job/runs/$RUN_ID"
else
    print_warning "Could not extract run ID from output"
fi

print_success "Workflow execution initiated"
