from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.app.models.assets import ImageAsset, ImageMetadata


class AssetRepository:
    def list_assets(self, db: Session, query: str = "", sort_by: str = "updated_at", order: str = "desc") -> list[ImageAsset]:
        stmt = select(ImageAsset).options(joinedload(ImageAsset.metadata_entry))
        assets = list(db.scalars(stmt).unique())
        terms = [term.strip().lower() for term in query.split() if term.strip()]
        if terms:
            filtered = []
            for asset in assets:
                metadata = asset.metadata_entry.search_text_normalized if asset.metadata_entry else ""
                haystack = f"{asset.original_filename.lower()} {metadata}"
                if all(term in haystack for term in terms):
                    filtered.append(asset)
            assets = filtered
        reverse = order != "asc"
        key_map = {
            "name": lambda item: (item.original_filename.lower(), item.id),
            "created_at": lambda item: (item.created_at.isoformat() if item.created_at else "", item.id),
            "updated_at": lambda item: (item.updated_at.isoformat() if item.updated_at else "", item.id),
        }
        key = key_map.get(sort_by, key_map["updated_at"])
        return sorted(assets, key=key, reverse=reverse)

    def get_asset(self, db: Session, asset_id: str) -> ImageAsset | None:
        stmt = select(ImageAsset).where(ImageAsset.id == asset_id).options(joinedload(ImageAsset.metadata_entry))
        return db.scalar(stmt)

    def ensure_metadata(self, asset: ImageAsset) -> ImageMetadata:
        if asset.metadata_entry is None:
            asset.metadata_entry = ImageMetadata(asset_id=asset.id, tags="", notes="", search_text_normalized=asset.original_filename.lower())
        return asset.metadata_entry
