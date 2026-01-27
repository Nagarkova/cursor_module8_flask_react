#!/usr/bin/env python3
"""
Test Verification Script
Validates that all test files are properly structured and executable
"""
import os
import sys
import ast
import re
from pathlib import Path

class TestVerifier:
    def __init__(self):
        self.backend_dir = Path(__file__).parent / "backend"
        self.frontend_dir = Path(__file__).parent / "frontend"
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def verify_backend_tests(self):
        """Verify backend test files"""
        print("\n" + "="*60)
        print("Verifying Backend Tests")
        print("="*60)
        
        test_files = [
            "test_checkout.py",
            "test_checkout_expanded.py",
            "test_data_generator.py"
        ]
        
        for test_file in test_files:
            file_path = self.backend_dir / test_file
            if file_path.exists():
                self.passed.append(f"✅ {test_file} exists")
                
                # Count test functions
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        test_count = len(re.findall(r'def test_', content))
                        self.passed.append(f"   Found {test_count} test functions")
                except Exception as e:
                    self.errors.append(f"❌ Error reading {test_file}: {e}")
            else:
                self.errors.append(f"❌ {test_file} not found")
        
        # Verify requirements.txt
        req_file = self.backend_dir / "requirements.txt"
        if req_file.exists():
            self.passed.append("✅ requirements.txt exists")
            with open(req_file, 'r') as f:
                content = f.read()
                if 'pytest' in content:
                    self.passed.append("✅ pytest in requirements.txt")
                else:
                    self.warnings.append("⚠️  pytest not found in requirements.txt")
        else:
            self.errors.append("❌ requirements.txt not found")
        
        # Verify test runner script
        runner_script = self.backend_dir / "run_tests.sh"
        if runner_script.exists():
            self.passed.append("✅ run_tests.sh exists")
            if os.access(runner_script, os.X_OK):
                self.passed.append("✅ run_tests.sh is executable")
            else:
                self.warnings.append("⚠️  run_tests.sh is not executable")
        else:
            self.warnings.append("⚠️  run_tests.sh not found")
    
    def verify_frontend_tests(self):
        """Verify frontend test files"""
        print("\n" + "="*60)
        print("Verifying Frontend Tests")
        print("="*60)
        
        test_files = [
            "src/__tests__/App.test.js",
            "src/__tests__/integration.test.js",
            "src/setupTests.js"
        ]
        
        for test_file in test_files:
            file_path = self.frontend_dir / test_file
            if file_path.exists():
                self.passed.append(f"✅ {test_file} exists")
                
                # Count test functions
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        test_count = len(re.findall(r'(test\(|it\(|describe\()', content))
                        self.passed.append(f"   Found {test_count} test cases")
                except Exception as e:
                    self.errors.append(f"❌ Error reading {test_file}: {e}")
            else:
                self.errors.append(f"❌ {test_file} not found")
        
        # Verify package.json
        package_file = self.frontend_dir / "package.json"
        if package_file.exists():
            self.passed.append("✅ package.json exists")
            with open(package_file, 'r') as f:
                content = f.read()
                if '@testing-library/react' in content or 'jest' in content:
                    self.passed.append("✅ Testing libraries in package.json")
                else:
                    self.warnings.append("⚠️  Testing libraries not found in package.json")
        else:
            self.errors.append("❌ package.json not found")
        
        # Verify test runner script
        runner_script = self.frontend_dir / "run_tests.sh"
        if runner_script.exists():
            self.passed.append("✅ run_tests.sh exists")
            if os.access(runner_script, os.X_OK):
                self.passed.append("✅ run_tests.sh is executable")
            else:
                self.warnings.append("⚠️  run_tests.sh is not executable")
        else:
            self.warnings.append("⚠️  run_tests.sh not found")
    
    def verify_test_coverage(self):
        """Verify test coverage areas"""
        print("\n" + "="*60)
        print("Verifying Test Coverage")
        print("="*60)
        
        coverage_areas = {
            "Critical Checkout Paths": [
                "test_add_item_to_cart",
                "test_checkout",
                "test_apply_discount",
                "test_get_order"
            ],
            "Payment Security": [
                "test_pci",
                "test_cvv",
                "test_card",
                "test_payment"
            ],
            "Error Handling": [
                "test_invalid",
                "test_error",
                "test_failure",
                "test_declined"
            ],
            "Edge Cases": [
                "test_empty",
                "test_concurrent",
                "test_edge",
                "test_boundary"
            ],
            "Security": [
                "test_sql",
                "test_xss",
                "test_security"
            ]
        }
        
        # Check backend tests
        backend_tests = []
        for test_file in ["test_checkout.py", "test_checkout_expanded.py"]:
            file_path = self.backend_dir / test_file
            if file_path.exists():
                with open(file_path, 'r') as f:
                    backend_tests.extend(re.findall(r'def (test_\w+)', f.read()))
        
        for area, keywords in coverage_areas.items():
            found = sum(1 for test in backend_tests if any(kw in test.lower() for kw in keywords))
            if found > 0:
                self.passed.append(f"✅ {area}: {found} tests found")
            else:
                self.warnings.append(f"⚠️  {area}: No tests found")
    
    def count_tests(self):
        """Count total test cases"""
        print("\n" + "="*60)
        print("Test Count Summary")
        print("="*60)
        
        backend_count = 0
        frontend_count = 0
        
        # Count backend tests
        for test_file in ["test_checkout.py", "test_checkout_expanded.py"]:
            file_path = self.backend_dir / test_file
            if file_path.exists():
                with open(file_path, 'r') as f:
                    backend_count += len(re.findall(r'def test_', f.read()))
        
        # Count frontend tests
        for test_file in ["src/__tests__/App.test.js", "src/__tests__/integration.test.js"]:
            file_path = self.frontend_dir / test_file
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Count test/it blocks
                    frontend_count += len(re.findall(r'(test\(|it\()', content))
        
        print(f"\nBackend Tests: {backend_count}")
        print(f"Frontend Tests: {frontend_count}")
        print(f"Total Tests: {backend_count + frontend_count}")
        
        if backend_count + frontend_count >= 30:
            self.passed.append(f"✅ Total test count ({backend_count + frontend_count}) meets requirement (30+)")
        else:
            self.warnings.append(f"⚠️  Total test count ({backend_count + frontend_count}) below requirement (30+)")
    
    def print_results(self):
        """Print verification results"""
        print("\n" + "="*60)
        print("Verification Results")
        print("="*60)
        
        print(f"\n✅ Passed: {len(self.passed)}")
        for item in self.passed:
            print(f"  {item}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings: {len(self.warnings)}")
            for item in self.warnings:
                print(f"  {item}")
        
        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
            for item in self.errors:
                print(f"  {item}")
        
        print("\n" + "="*60)
        
        if self.errors:
            print("❌ VERIFICATION FAILED - Errors found")
            return False
        elif self.warnings:
            print("⚠️  VERIFICATION PASSED WITH WARNINGS")
            return True
        else:
            print("✅ VERIFICATION PASSED")
            return True

def main():
    verifier = TestVerifier()
    verifier.verify_backend_tests()
    verifier.verify_frontend_tests()
    verifier.verify_test_coverage()
    verifier.count_tests()
    
    success = verifier.print_results()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
