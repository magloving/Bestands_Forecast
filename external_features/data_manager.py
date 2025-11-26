"""
Data Manager für Hybrid-Strategie.

Verwaltet Feature-Export als finale CSV-Snapshots.
Trennt Development (Cache) von Production (CSV).
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import os


class FeatureDataManager:
    """
    Verwaltet Feature-Daten nach Hybrid-Strategie.
    
    Strategie:
    - Development: Automatisches Caching (cache/)
    - Production: Finale CSV-Snapshots (data/)
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialisiert Data Manager.
        
        Args:
            data_dir: Verzeichnis für finale CSV-Exports
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def export_training_snapshot(
        self,
        features_df: pd.DataFrame,
        name: str = "training",
        overwrite: bool = False
    ) -> Path:
        """
        Exportiert finales Training-Dataset als CSV-Snapshot.
        
        Args:
            features_df: Feature DataFrame
            name: Name des Snapshots (z.B. "training", "test", "2024_Q1")
            overwrite: Existierende Datei überschreiben?
            
        Returns:
            Path zum exportierten CSV
            
        Raises:
            FileExistsError: Wenn Datei existiert und overwrite=False
        """
        filename = f"external_features_{name}.csv"
        filepath = self.data_dir / filename
        
        # Check if exists
        if filepath.exists() and not overwrite:
            raise FileExistsError(
                f"❌ Snapshot existiert bereits: {filepath}\n"
                f"   Nutze overwrite=True zum Überschreiben, oder\n"
                f"   wähle einen anderen Namen."
            )
        
        # Export
        features_df.to_csv(filepath, index=False)
        
        # Stats
        file_size = os.path.getsize(filepath) / 1024  # KB
        
        print("="*70)
        print("✅ SNAPSHOT EXPORTIERT")
        print("="*70)
        print(f"Datei:     {filepath}")
        print(f"Shape:     {features_df.shape}")
        print(f"Größe:     {file_size:.1f} KB")
        print(f"Zeitraum:  {features_df['date'].min()} bis {features_df['date'].max()}")
        print("\n💡 Nächste Schritte:")
        print(f"   1. git add {filepath}")
        print(f"   2. git commit -m 'Add {name} feature snapshot'")
        print(f"   3. git push origin main")
        
        return filepath
    
    def load_snapshot(self, name: str) -> pd.DataFrame:
        """
        Lädt einen existierenden Snapshot.
        
        Args:
            name: Name des Snapshots
            
        Returns:
            Feature DataFrame
            
        Raises:
            FileNotFoundError: Wenn Snapshot nicht existiert
        """
        filename = f"external_features_{name}.csv"
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(
                f"❌ Snapshot nicht gefunden: {filepath}\n"
                f"   Verfügbare Snapshots: {self.list_snapshots()}"
            )
        
        df = pd.read_csv(filepath, parse_dates=['date'])
        
        print(f"✅ Snapshot geladen: {name}")
        print(f"   Shape: {df.shape}")
        print(f"   Zeitraum: {df['date'].min()} bis {df['date'].max()}")
        
        return df
    
    def list_snapshots(self) -> List[str]:
        """
        Listet alle verfügbaren Snapshots.
        
        Returns:
            Liste von Snapshot-Namen
        """
        pattern = "external_features_*.csv"
        files = list(self.data_dir.glob(pattern))
        
        # Extract names
        names = []
        for f in files:
            # external_features_training.csv → training
            name = f.stem.replace("external_features_", "")
            names.append(name)
        
        return sorted(names)
    
    def create_combined_dataset(
        self,
        retail_csv: str,
        feature_snapshot: str,
        output_name: str = "combined_training"
    ) -> Path:
        """
        Kombiniert Retail-Daten mit Feature-Snapshot.
        
        Args:
            retail_csv: Pfad zu retail_store_inventory.csv
            feature_snapshot: Name des Feature-Snapshots
            output_name: Name des Output-CSV
            
        Returns:
            Path zum kombinierten Dataset
        """
        # Load retail data
        df_retail = pd.read_csv(retail_csv)
        df_retail['Date'] = pd.to_datetime(df_retail['Date'])
        
        # Load features
        df_features = self.load_snapshot(feature_snapshot)
        
        # Merge
        df_combined = df_retail.merge(
            df_features,
            left_on='Date',
            right_on='date',
            how='left'
        )
        
        # Export
        output_file = self.data_dir / f"{output_name}.csv"
        df_combined.to_csv(output_file, index=False)
        
        print("="*70)
        print("✅ KOMBINIERTES DATASET ERSTELLT")
        print("="*70)
        print(f"Retail Data:  {df_retail.shape}")
        print(f"Features:     {df_features.shape}")
        print(f"Combined:     {df_combined.shape}")
        print(f"Output:       {output_file}")
        
        return output_file
    
    def snapshot_info(self):
        """Zeigt Übersicht aller Snapshots."""
        snapshots = self.list_snapshots()
        
        print("="*70)
        print("📊 VERFÜGBARE FEATURE SNAPSHOTS")
        print("="*70)
        
        if not snapshots:
            print("❌ Keine Snapshots gefunden!")
            print("\n💡 Erstelle Snapshots mit export_training_snapshot()")
            return
        
        for name in snapshots:
            filepath = self.data_dir / f"external_features_{name}.csv"
            df = pd.read_csv(filepath, parse_dates=['date'])
            file_size = os.path.getsize(filepath) / 1024
            
            print(f"\n📄 {name}")
            print(f"   Shape:     {df.shape}")
            print(f"   Zeitraum:  {df['date'].min().date()} bis {df['date'].max().date()}")
            print(f"   Größe:     {file_size:.1f} KB")
            print(f"   Columns:   {', '.join(df.columns[:5])}...")
