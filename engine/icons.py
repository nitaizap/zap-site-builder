"""Inline line icons (24px grid, stroke = currentColor). Hand-drawn for this project; no icon font."""

PATHS = {
    "check": '<path d="M5 12.5l4.2 4.2L19 7"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.6-3 8.4-7 10-4-1.6-7-5.4-7-10V6z"/><path d="M8.8 12l2.2 2.2 4.2-4.4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8"/><path d="M14.7 6.3L13 4.6a4 4 0 0 0-5.6 5.6l1.7 1.7L3 18l3 3 6.1-6.1"/>',
    "tools": '<path d="M3 21l7-7"/><path d="M14 4l6 6-3 3-6-6z"/><path d="M5 5l4 4"/><path d="M3 7l4-4"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14L7 21l5-2.5 5 2.5-1.5-7"/>',
    "truck": '<path d="M2 6h11v10H2zM13 10h4l4 3.5V16h-8"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    "droplet": '<path d="M12 3s6.5 7 6.5 11.5a6.5 6.5 0 0 1-13 0C5.5 10 12 3 12 3z"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "leaf": '<path d="M5 19C5 9 11 4 20 4c0 9-5 15-15 15z"/><path d="M5 19l8-8"/>',
    "heart": '<path d="M12 20s-8-4.7-8-10.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 8 2.5C20 15.3 12 20 12 20z"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "map": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    "document": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "lock": '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16l.7 1.8 1.8.7-1.8.7L19 21l-.7-1.8-1.8-.7 1.8-.7z"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "money": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 9v.01M18 15v.01"/>',
    "car": '<path d="M3 16v-4l2-5h14l2 5v4z"/><path d="M3 12h18"/><circle cx="7" cy="16.5" r="1.8"/><circle cx="17" cy="16.5" r="1.8"/>',
    "scooter": '<circle cx="5.5" cy="17.5" r="2.3"/><circle cx="18.5" cy="17.5" r="2.3"/><path d="M2 7h6v5H2zM5 12v3M7.8 17.5H14l3-6.5h-2.5M17 11l-1.6-4.5H13"/>',
    "van": '<path d="M2 6h12l4 4h3.5v6.5H2z"/><path d="M14 6v4h4M2 12h19.5"/><circle cx="6.5" cy="17" r="1.9"/><circle cx="17" cy="17" r="1.9"/>',
    "scale": '<path d="M12 3v18M7 21h10M4 7h16"/><path d="M4 7l-2.5 6a3 3 0 0 0 5 0zM20 7l-2.5 6a3 3 0 0 0 5 0z"/>',
    "medical": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 8v8M8 12h8"/>',
    "star-badge": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5l1.3 2.8 3 .3-2.3 2 .7 3-2.7-1.6-2.7 1.6.7-3-2.3-2 3-.3z"/>',
    "thumb": '<path d="M7 11v9H3v-9zM7 11l4-8a2.5 2.5 0 0 1 2.5 2.5V9H19a2 2 0 0 1 2 2.3l-1.2 7A2 2 0 0 1 17.8 20H7"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 3 2.5 15 0 18M12 3c-2.5 3-2.5 15 0 18"/>',
}


def icon_svg(name):
    p = PATHS.get(name, PATHS["check"])
    return ('<svg class="zs-svg" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            + p + "</svg>")
