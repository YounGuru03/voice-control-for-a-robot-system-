# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Voice Control System
Builds a standalone Windows executable with all dependencies
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect Whisper model files and data
whisper_datas = collect_data_files('whisper')

# Collect torch and related data
torch_datas = collect_data_files('torch')

# Collect all submodules
hiddenimports = [
    'whisper',
    'torch',
    'torchaudio',
    'sounddevice',
    'soundfile',
    'numpy',
    'scipy',
    'yaml',
    'difflib',
    'hashlib',
    'agents',
    'agents.base_agent',
    'agents.input_agent',
    'agents.recognition_agent',
    'agents.command_parser_agent',
    'agents.speaker_id_agent',
    'agents.logging_agent',
]

# Add all torch submodules
hiddenimports.extend(collect_submodules('torch'))
hiddenimports.extend(collect_submodules('torchaudio'))

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        *whisper_datas,
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'PIL',
        'tkinter',
        'PyQt5',
        'pandas',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VoiceControl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VoiceControl',
)
