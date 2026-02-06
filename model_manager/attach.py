# -*- coding: utf-8 -*-
import os
import sqlite3

from qgis.core import QgsProject
from qgis.utils import iface


def attach_registry():
    """
    Attaches the model registry GeoPackage (GPKG) as a SQLite database
    """
    
    gpkg_path = "/path/to/model_registry.gpkg"

    if not os.path.exists(gpkg_path):
        iface.messageBar().pushCritical(
            "Model Manager",
            f"Registry GPKG not found: {gpkg_path}"
        )
        return

    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    try:
        cur.execute(f"ATTACH DATABASE '{gpkg_path}' AS model_registry")
        iface.messageBar().pushInfo(
            "Model Manager",
            "Model registry has been successfully attached"
        )
    except Exception as e:
        iface.messageBar().pushCritical(
            "Model Manager",
            f"Failed to attach registry: {e}"
        )
