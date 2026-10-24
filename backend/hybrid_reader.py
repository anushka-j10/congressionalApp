"""Run local and vision readers; preserve actual candidates and disagreement."""

from backend.readers import ReaderError, Reading
from backend.reader_tokens import compare_candidates


class HybridReader:
    name = "hybrid"

    def __init__(self, local_reader, vision_reader):
        self.local = local_reader
        self.vision = vision_reader

    def read(self, jpeg):
        results, warnings = {}, []
        for reader in (self.local, self.vision):
            try:
                results[reader.name] = reader.read(jpeg)
                warnings.extend(results[reader.name].warnings)
            except ReaderError:
                warnings.append(f"The {reader.name} reader failed. Its agreement check is unavailable.")
        if not results:
            raise ReaderError("Both text readers failed. Try another photo or try again later.")
        local = results.get(self.local.name)
        vision = results.get(self.vision.name)
        primary = local if local and local.text.strip() else (vision or local)
        reviews = compare_candidates(local.text if local else "", vision.text if vision else "",
                                     self.local.name, self.vision.name)
        warnings.append("Reader agreement is not verification. Check every disputed value against the photo.")
        return Reading(primary.text, warnings, reviews,
                       self.local.name if primary is local else self.vision.name)
