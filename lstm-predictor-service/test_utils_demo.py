# test_utils_demo.py
"""
Quick validation script for LSTM utils.
Tests metrics, preprocessing, and feature engineering without pytest.
Run: python test_utils_demo.py
"""

import numpy as np
import pandas as pd
from pathlib import Path
from colorama import Fore, Back, Style, init

init(autoreset=True)

# Import utils
from app.utils.metrics import mae, mse, rmse
from app.utils.feature_engineering import create_sequences, normalize_data, denormalize_data
from app.models.preprocessor import DataPreprocessor, prepare_prediction_input


def print_section(title):
    """Pretty print section header."""
    print(f"\n{Back.CYAN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}  {title}{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}")


def test_metrics():
    """Test MAE, MSE, RMSE calculations."""
    print_section("TEST 1: Metrics (MAE, MSE, RMSE)")
    
    # Sample predictions vs actual
    y_true = np.array([10.0, 20.0, 15.0, 25.0, 30.0])
    y_pred = np.array([9.5, 21.0, 14.5, 24.0, 31.0])
    
    print(f"\nActual values:     {y_true}")
    print(f"Predicted values:  {y_pred}")
    
    mae_score = mae(y_true, y_pred)
    mse_score = mse(y_true, y_pred)
    rmse_score = rmse(y_true, y_pred)
    
    print(f"\n{Fore.GREEN}✓ MAE:  {mae_score:.4f}")
    print(f"{Fore.GREEN}✓ MSE:  {mse_score:.4f}")
    print(f"{Fore.GREEN}✓ RMSE: {rmse_score:.4f}")
    
    assert mae_score > 0, "MAE should be positive"
    assert mse_score > 0, "MSE should be positive"
    assert rmse_score > 0, "RMSE should be positive"
    assert rmse_score == np.sqrt(mse_score), "RMSE should equal sqrt(MSE)"
    
    print(f"{Fore.GREEN}✅ All metrics tests passed!")


def test_normalization():
    """Test data normalization and denormalization."""
    print_section("TEST 2: Normalization & Denormalization")
    
    # Create sample edge traffic data (5 edges)
    raw_data = np.array([
        [18.93, 10.13, 5.23, 4.14, 3.08],
        [24.02, 11.01, 8.98, 5.42, 4.26],
        [22.14, 9.34, 5.62, 4.57, 3.81]
    ], dtype=np.float32)
    
    print(f"\nRaw data shape: {raw_data.shape}")
    print(f"Raw data (first edge):\n{raw_data[:, 0]}")
    print(f"Raw data range: [{raw_data.min():.2f}, {raw_data.max():.2f}]")
    
    # Normalize
    normalized, scaler = normalize_data(raw_data)
    
    print(f"\nNormalized data range: [{normalized.min():.2f}, {normalized.max():.2f}]")
    print(f"Normalized data (first edge):\n{normalized[:, 0]}")
    
    assert np.allclose(normalized.min(), 0.0, atol=1e-4), "Normalized min should be ~0"
    assert np.allclose(normalized.max(), 1.0, atol=1e-4), "Normalized max should be ~1"
    
    # Denormalize
    reconstructed = denormalize_data(normalized, scaler)
    
    print(f"\nReconstructed data (first edge):\n{reconstructed[:, 0]}")
    
    # Check reconstruction accuracy
    error = np.mean(np.abs(raw_data - reconstructed))
    print(f"Mean reconstruction error: {error:.6f}")
    
    assert error < 1e-4, "Reconstruction error should be near zero"
    
    print(f"{Fore.GREEN}✅ All normalization tests passed!")


def test_sequence_creation():
    """Test sliding window sequence creation."""
    print_section("TEST 3: Sequence Creation")
    
    # Create simple sample data (10 timesteps, 5 features)
    raw_data = np.random.rand(10, 5) * 30  # Random density values 0-30
    
    # Normalize
    normalized, _ = normalize_data(raw_data)
    
    print(f"\nRaw data shape: {raw_data.shape} (timesteps, features)")
    
    # Create sequences (3 timesteps → 1 forecast)
    X, y = create_sequences(normalized, seq_length=3)
    
    print(f"\nSequence parameters:")
    print(f"  seq_length: 3 (input timesteps)")
    print(f"  Expected sequences: {len(raw_data) - 3} (10 - 3)")
    
    print(f"\n{Fore.CYAN}X shape: {X.shape} (samples, timesteps, features)")
    print(f"{Fore.CYAN}y shape: {y.shape} (samples, features)")
    
    assert X.shape == (7, 3, 5), f"Expected X shape (7, 3, 5), got {X.shape}"
    assert y.shape == (7, 5), f"Expected y shape (7, 5), got {y.shape}"
    
    # Verify sliding window logic
    print(f"\nSequence example:")
    print(f"  Input (3 timesteps):  {X[0]}")
    print(f"  Target (1 timestep):  {y[0]}")
    
    print(f"{Fore.GREEN}✅ All sequence tests passed!")


def test_preprocessor():
    """Test DataPreprocessor class."""
    print_section("TEST 4: DataPreprocessor Class")
    
    # Initialize
    preprocessor = DataPreprocessor()
    print(f"\n{Fore.GREEN}✓ DataPreprocessor initialized")
    
    # Sample data
    raw_data = np.array([
        [18.93, 10.13, 5.23, 4.14, 3.08],
        [24.02, 11.01, 8.98, 5.42, 4.26],
        [22.14, 9.34, 5.62, 4.57, 3.81],
        [20.50, 10.75, 6.10, 4.90, 3.50]
    ], dtype=np.float32)
    
    # Fit scaler
    normalized = preprocessor.fit_scaler(raw_data)
    print(f"{Fore.GREEN}✓ Fitted scaler on {raw_data.shape[0]} samples")
    
    # Create sequences
    X, y = DataPreprocessor.create_sequences(normalized, seq_length=3)
    print(f"{Fore.GREEN}✓ Created {len(X)} sequences")
    
    # Test prediction input preparation
    recent_data = [
        [18.93, 10.13, 5.23, 4.14, 3.08],
        [24.02, 11.01, 8.98, 5.42, 4.26],
        [22.14, 9.34, 5.62, 4.57, 3.81]
    ]
    
    batch_input = prepare_prediction_input(recent_data, preprocessor)
    print(f"{Fore.GREEN}✓ Prepared prediction input shape: {batch_input.shape}")
    
    assert batch_input.shape == (1, 3, 5), f"Expected (1, 3, 5), got {batch_input.shape}"
    
    # Test denormalization
    denorm = preprocessor.denormalize(batch_input[0])
    print(f"{Fore.GREEN}✓ Denormalized prediction: {denorm}")
    
    print(f"{Fore.GREEN}✅ All preprocessor tests passed!")


def test_edge_data_load():
    """Test loading and analyzing edge data (if available)."""
    print_section("TEST 5: Edge Data Loading (Optional)")
    
    edge_xml_path = Path("SUMO/Results/MAPPO/edgeData.xml")
    
    if not edge_xml_path.exists():
        print(f"\n{Fore.YELLOW}⚠️  {edge_xml_path} not found. Skipping edge data test.")
        print(f"{Fore.YELLOW}   (This is OK — edge data is optional for this validation)")
        return
    
    import xml.etree.ElementTree as ET
    
    print(f"\n{Fore.GREEN}✓ Loading {edge_xml_path}")
    
    try:
        tree = ET.parse(edge_xml_path)
        root = tree.getroot()
        
        edges_data = []
        for interval in root.findall('interval')[:100]:  # First 100 intervals
            for edge in interval.findall('edge'):
                edges_data.append({
                    'density': float(edge.get('density', 0))
                })
        
        if edges_data:
            densities = np.array([e['density'] for e in edges_data])
            print(f"{Fore.GREEN}✓ Loaded {len(edges_data)} edge measurements")
            print(f"{Fore.CYAN}  Density range: [{densities.min():.2f}, {densities.max():.2f}]")
            print(f"{Fore.CYAN}  Density mean: {densities.mean():.2f}")
            print(f"{Fore.GREEN}✅ Edge data loading test passed!")
        else:
            print(f"{Fore.YELLOW}⚠️  No edge data found in XML")
    
    except Exception as e:
        print(f"{Fore.YELLOW}⚠️  Error loading edge data: {e}")
        print(f"{Fore.YELLOW}   (This is OK — edge data is optional)")


def main():
    """Run all validation tests."""
    print(f"\n{Back.MAGENTA}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}  LSTM Utils Validation Suite{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    
    try:
        test_metrics()
        test_normalization()
        test_sequence_creation()
        test_preprocessor()
        test_edge_data_load()
        
        print(f"\n{Back.GREEN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.BLACK}  ✅ ALL TESTS PASSED!{Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.BLACK}{'='*60}{Style.RESET_ALL}\n")
        
    except AssertionError as e:
        print(f"\n{Back.RED}{Fore.WHITE}❌ TEST FAILED: {e}{Style.RESET_ALL}\n")
        return False
    except Exception as e:
        print(f"\n{Back.RED}{Fore.WHITE}❌ ERROR: {e}{Style.RESET_ALL}\n")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)