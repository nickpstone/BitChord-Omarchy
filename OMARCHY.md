# BitChord on Omarchy

This fork uses the existing Kotlin/Compose desktop application. Its audio engine uses FFmpeg and Java Sound, with session-bus MPRIS controls and a StatusNotifier tray icon. Omarchy runs its AWT window through XWayland. This is a Linux desktop application, not an Android emulator or web wrapper; it does not yet use a native Wayland window backend.

Linux x86_64 and ARM64 (aarch64, including Apple Silicon Macs running Asahi Linux) are both supported. The build selects the matching FFmpeg, JavaFX and Skiko natives for the host. On ARM64, JavaFX is 21.0.12, because Maven Central only carries `linux-aarch64` JavaFX jars from 21.0.11 onwards; x86_64 stays on 21.0.10.

## Build and install

Install the build tools (the script never runs sudo):

```bash
sudo pacman -S --needed jdk21-openjdk cmake gcc ninja
./scripts/omarchy setup
```

Java 21 is required to build. The script selects `/usr/lib/jvm/java-21-openjdk` unless `JAVA_HOME` is already set. If another JDK is selected, run:

```bash
JAVA_HOME=/usr/lib/jvm/java-21-openjdk ./scripts/omarchy setup
```

The build downloads Gradle, Maven dependencies, native codecs, and analysis assets. It runs the shared data, shared UI, and desktop tests before packaging. No Android SDK is required: `-Pbitchord.android=false` disables Android targets in all modules.

`setup` installs only after the build and tests succeed. The resulting application contains its Java runtime and codecs. Installed builds need the usual Omarchy desktop libraries (XWayland, GTK 3, GL, ALSA and the session D-Bus), but no system JDK.

Open **BitChord** from the application menu, or run `~/.local/bin/bitchord`. Restart a running instance after updating.

The `Omarchy desktop` GitHub workflow also builds and tests this SDK-free path on Linux.

## Development

```bash
./scripts/omarchy run      # run from source
./scripts/omarchy build    # test and create the app bundle
./scripts/omarchy install  # install an already-built bundle
```

The source bundle is `desktopApp/build/compose/binaries/main/app/BitChord`. For Android development, use `-Pbitchord.android=true` with a configured SDK; ordinary Gradle invocations retain SDK autodetection.

## Desktop integration

- The menu entry is `bitchord.desktop`, matching MPRIS’s `DesktopEntry`.
- The window class is `BitChord`, for launcher grouping and existing window rules.
- The launcher sets `_JAVA_AWT_WM_NONREPARENTING=1` for tiling window managers.
- MPRIS uses `org.mpris.MediaPlayer2.bitchord`. Existing Omarchy media keys and `playerctl --player=bitchord play-pause` can control it.
- The tray supports returning to the window while playback continues. Closing behavior depends on whether the tray is available.
- Startup does not check upstream releases or display an update prompt.
- Text starts at 125% size. Open Settings → Appearance → Font size to choose 100–150%; changes apply immediately and persist after restarting.
- No Hyprland configuration or keybindings are changed.

The existing desktop features include music browsing and search, local music, playlists, downloads, lyrics, account integrations, audio controls, and source modules. Network-dependent features still depend on their upstream services and any required account or module configuration.

## Installed files

| Purpose | Default location |
| --- | --- |
| Application and bundled runtime | `~/.local/share/bitchord/app` |
| Launcher | `~/.local/bin/bitchord` |
| Menu entry | `~/.local/share/applications/bitchord.desktop` |
| Icon | `~/.local/share/icons/hicolor/512x512/apps/bitchord.png` |
| Logs | `~/.local/state/bitchord/desktop.log` |
| Cache | `~/.cache/bitchord` |

`XDG_DATA_HOME` controls application, menu, and icon locations. `BITCHORD_BIN_HOME` overrides the launcher directory. Existing desktop settings and music files are retained across installation.

## Troubleshooting

If the menu entry does not appear, launch `~/.local/bin/bitchord` and check that the entry exists in your XDG applications directory. If startup fails, run the launcher in a terminal and inspect `~/.local/state/bitchord/desktop.log`.

For a blank window, verify XWayland is running and the graphics driver supports OpenGL. For missing media controls, check the session D-Bus and `playerctl -l` while BitChord is open. The app must run as your desktop user, not with sudo.

## Verification

Verified locally on Omarchy on 2026-10-16:

- Desktop-only build and bundled runtime packaging succeeded without an Android SDK.
- 46 shared data, 34 shared UI, and 342 desktop tests passed, with no failures or skips.
- Two isolated installer checks passed, including upgrades, paths with spaces, launcher arguments, and preserving settings.
- The installed desktop entry passed `desktop-file-validate`.
- The packaged app launched, displayed live home content and artwork, and rendered in a tiled Hyprland window.
- Hyprland reported class `BitChord` with XWayland enabled; the session bus reported MPRIS identity `BitChord` and playback status `Stopped`.

Account sign-in and playback through the physical speakers were not manually verified. `playerctl` was not installed on the verification machine; MPRIS was checked directly with `busctl`.

ARM64 verified locally on Omarchy (Asahi Linux, MacBook Air M2, 16K pages) on 2026-10-17:

- The same 46 shared data, 34 shared UI, and 342 desktop tests passed, with no failures or skips.
- The packaged launcher and all bundled native libraries are aarch64.
- The installed desktop entry passed `desktop-file-validate`.
- The packaged app launched in a Hyprland window via XWayland, the JavaFX WebKit PoToken setup completed, and the session bus reported MPRIS identity `org.mpris.MediaPlayer2.bitchord`.

Account sign-in and audio playback were not manually verified on ARM64.
