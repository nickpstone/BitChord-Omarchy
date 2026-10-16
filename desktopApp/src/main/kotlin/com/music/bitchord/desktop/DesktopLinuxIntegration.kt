package com.music.bitchord.desktop

import java.awt.Toolkit

/** Stable XWayland identity for the desktop entry and tiling window manager. */
internal object DesktopLinuxIntegration {
    fun install() {
        if (!DesktopPlatform.isLinux) return
        // AWT derives WM_CLASS from the JVM entry class instead of the application name.
        // Set it before the first window creates a native peer. The packaged launcher opens
        // this one JDK package; other toolkits (including a future Wayland backend) are skipped.
        runCatching {
            val toolkit = Toolkit.getDefaultToolkit()
            if (toolkit.javaClass.name == "sun.awt.X11.XToolkit") {
                toolkit.javaClass.getDeclaredField("awtAppClassName").apply {
                    isAccessible = true
                    set(null, "BitChord")
                }
            }
        }.onFailure {
            DesktopTrackLog.log("Linux application identity unavailable: ${it.message}")
        }
    }
}
