# BitChord for Omarchy

<!-- impeccable:product-schema 1 -->

## Platform

adaptive

## Users and purpose

Omarchy desktop users listening to music, browsing their library, and controlling playback alongside other desktop applications.

## Stack

Existing Kotlin Multiplatform data and UI modules with a Compose Desktop JVM application. The user confirmed adapting the existing desktop app while preserving its music features.

## Operating context

Primary target: Omarchy Linux with Hyprland, XWayland, a session D-Bus, and desktop audio. The current Compose AWT window uses XWayland. Android sources are retained, but the Omarchy build must not require an Android SDK.

## Capabilities and constraints

Preserve existing music search, playback, local library, playlists, downloads, lyrics, accounts, and module sources. Reuse existing MPRIS and StatusNotifier integrations. Installation is per user, includes the runtime, and exposes a menu entry and command. Do not modify desktop settings or keybindings during installation.

## Brand commitments

Retain the BitChord name, logo, and existing desktop interface for this adaptation. A visual redesign was not requested or approved.

## Evidence on hand

`desktopApp/`, `shared/`, and `sharedUi/` contain the existing implementation and tests. `DESKTOP.md` describes upstream desktop behavior. `OMARCHY.md` describes this fork’s installation path. Network service availability must be verified independently from successful compilation.
