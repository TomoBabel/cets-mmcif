import os
import logging

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=[
            str(Path(__file__).parents[1] / ".env"), 
        ],
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    output_mmcif_directory: Path = Path(__file__).parents[1] / "output_data" / "cets-mmcif"
    validation_dictionary_path: Path = Path(__file__).parents[1] / "resources" / "mmcif_pdbx_v50.dic"


def get_settings():
    return Settings() 
