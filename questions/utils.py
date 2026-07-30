def sanitize_tags(tags_str):
    if not tags_str:
        return ""
    return ", ".join([t.strip().lower() for t in tags_str.split(",") if t.strip()])
