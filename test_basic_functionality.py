"""
Basic functionality test without requiring dependencies
Tests the system structure and configuration
"""

import os
import sys
import yaml


def test_project_structure():
    """Test that all required files exist"""
    print("\n" + "="*60)
    print("Testing Project Structure")
    print("="*60)
    
    required_files = [
        'main.py',
        'requirements.txt',
        'setup.py',
        'voice_control.spec',
        'config/settings.yaml',
        'config/commands.yaml',
        'agents/__init__.py',
        'agents/base_agent.py',
        'agents/input_agent.py',
        'agents/recognition_agent.py',
        'agents/command_parser_agent.py',
        'agents/speaker_id_agent.py',
        'agents/logging_agent.py',
        '.github/workflows/build-windows-exe.yml',
        'README.md',
        'ARCHITECTURE.md',
        'USAGE.md',
        'CONTRIBUTING.md',
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
            print(f"  ✗ Missing: {file_path}")
        else:
            print(f"  ✓ Found: {file_path}")
    
    if missing:
        print(f"\n✗ {len(missing)} files missing")
        return False
    else:
        print(f"\n✓ All {len(required_files)} required files present")
        return True


def test_python_syntax():
    """Test that all Python files have valid syntax"""
    print("\n" + "="*60)
    print("Testing Python Syntax")
    print("="*60)
    
    python_files = [
        'main.py',
        'setup.py',
        'test_system.py',
        'agents/base_agent.py',
        'agents/input_agent.py',
        'agents/recognition_agent.py',
        'agents/command_parser_agent.py',
        'agents/speaker_id_agent.py',
        'agents/logging_agent.py',
    ]
    
    import py_compile
    errors = []
    
    for file_path in python_files:
        try:
            py_compile.compile(file_path, doraise=True)
            print(f"  ✓ {file_path}")
        except py_compile.PyCompileError as e:
            errors.append((file_path, str(e)))
            print(f"  ✗ {file_path}: {e}")
    
    if errors:
        print(f"\n✗ {len(errors)} syntax errors")
        return False
    else:
        print(f"\n✓ All {len(python_files)} Python files have valid syntax")
        return True


def test_yaml_configuration():
    """Test that YAML configuration files are valid"""
    print("\n" + "="*60)
    print("Testing YAML Configuration")
    print("="*60)
    
    yaml_files = [
        'config/settings.yaml',
        'config/commands.yaml',
    ]
    
    errors = []
    for file_path in yaml_files:
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            print(f"  ✓ {file_path}")
            
            # Check specific structure
            if 'settings.yaml' in file_path:
                required_sections = ['audio', 'whisper', 'speaker_id', 'commands', 'logging']
                for section in required_sections:
                    if section not in data:
                        print(f"    ⚠ Missing section: {section}")
            
            if 'commands.yaml' in file_path:
                if 'commands' not in data:
                    errors.append((file_path, "Missing 'commands' section"))
                else:
                    print(f"    → {len(data['commands'])} commands defined")
                if 'aliases' in data:
                    print(f"    → {len(data['aliases'])} aliases defined")
                    
        except Exception as e:
            errors.append((file_path, str(e)))
            print(f"  ✗ {file_path}: {e}")
    
    if errors:
        print(f"\n✗ {len(errors)} YAML errors")
        return False
    else:
        print(f"\n✓ All YAML files are valid")
        return True


def test_requirements():
    """Test that requirements.txt is valid"""
    print("\n" + "="*60)
    print("Testing Requirements")
    print("="*60)
    
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        
        requirements = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        print(f"  Total requirements: {len(requirements)}")
        
        essential = ['whisper', 'torch', 'numpy', 'sounddevice', 'pyyaml', 'pyinstaller']
        found = []
        
        for req in essential:
            if any(req in line for line in requirements):
                found.append(req)
                print(f"  ✓ {req}")
            else:
                print(f"  ✗ Missing: {req}")
        
        if len(found) == len(essential):
            print(f"\n✓ All essential requirements present")
            return True
        else:
            print(f"\n✗ Missing {len(essential) - len(found)} essential requirements")
            return False
            
    except Exception as e:
        print(f"  ✗ Error reading requirements.txt: {e}")
        return False


def test_github_actions():
    """Test GitHub Actions workflow configuration"""
    print("\n" + "="*60)
    print("Testing GitHub Actions Workflow")
    print("="*60)
    
    workflow_path = '.github/workflows/build-windows-exe.yml'
    
    try:
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        required_elements = [
            'runs-on: windows-latest',
            'pyinstaller voice_control.spec',
            'python-version',
            'upload-artifact',
        ]
        
        missing = []
        for element in required_elements:
            if element in content:
                print(f"  ✓ Contains: {element}")
            else:
                missing.append(element)
                print(f"  ✗ Missing: {element}")
        
        if missing:
            print(f"\n✗ Workflow missing {len(missing)} required elements")
            return False
        else:
            print("\n✓ GitHub Actions workflow properly configured")
            return True
            
    except Exception as e:
        print(f"  ✗ Error reading workflow file: {e}")
        return False


def test_documentation():
    """Test documentation completeness"""
    print("\n" + "="*60)
    print("Testing Documentation")
    print("="*60)
    
    docs = {
        'README.md': ['Installation', 'Usage', 'Features'],
        'ARCHITECTURE.md': ['Agent', 'Architecture'],
        'USAGE.md': ['Quick Start', 'Command'],
        'CONTRIBUTING.md': ['Contributing', 'Development'],
    }
    
    all_good = True
    for doc_file, keywords in docs.items():
        try:
            with open(doc_file, 'r') as f:
                content = f.read().lower()
            
            found = sum(1 for keyword in keywords if keyword.lower() in content)
            if found == len(keywords):
                print(f"  ✓ {doc_file}: {found}/{len(keywords)} sections")
            else:
                print(f"  ⚠ {doc_file}: {found}/{len(keywords)} sections")
                all_good = False
                
        except Exception as e:
            print(f"  ✗ {doc_file}: {e}")
            all_good = False
    
    if all_good:
        print("\n✓ Documentation complete")
    else:
        print("\n⚠ Some documentation sections missing")
    
    return all_good


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Voice Control System - Basic Functionality Tests")
    print("="*60)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Python Syntax", test_python_syntax),
        ("YAML Configuration", test_yaml_configuration),
        ("Requirements", test_requirements),
        ("GitHub Actions", test_github_actions),
        ("Documentation", test_documentation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n✓ All basic functionality tests passed!")
        print("System structure is valid and ready for use.")
        return 0
    else:
        print(f"\n✗ {len(tests) - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
