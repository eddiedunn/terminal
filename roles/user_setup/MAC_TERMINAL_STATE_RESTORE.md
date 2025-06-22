# Disabling macOS Terminal State Restore (While Keeping Zsh History)

macOS Terminal apps (Terminal.app and iTerm2) may save and restore the state of terminal windows—including scrollback and sometimes command history—independently of your shell's own history mechanism. This can cause commands to reappear in new terminal sessions, even after clearing your shell history.

This document explains how to disable this feature while keeping your Zsh history fully functional.

## Why This Matters
- **Zsh's own history** (usually `~/.zsh_history`) is managed by the shell and is not affected by macOS state restore.
- **macOS state restore** can cause confusion by restoring previous terminal content, even if you clear your Zsh history.

## Disabling State Restore for Terminal.app

1. **Prevent Terminal from restoring windows on quit:**

   ```sh
   defaults write com.apple.Terminal NSQuitAlwaysKeepsWindows -bool false
   ```

2. **Delete existing saved state:**

   ```sh
   rm -rf ~/Library/Saved\ Application\ State/com.apple.Terminal.savedState/
   ```

## Disabling State Restore for iTerm2

1. **Turn off window arrangement restore:**
   - Open iTerm2 Preferences → General → "Open profiles in new windows"
   - Make sure **"Save window arrangement on quit"** is **unchecked**.

2. **Delete existing saved state:**

   ```sh
   rm -rf ~/Library/Saved\ Application\ State/com.googlecode.iterm2.savedState/
   ```

## Notes
- These changes affect only the terminal app's state restore. Your Zsh history (`~/.zsh_history`) will continue to function as normal.
- If you use other terminal emulators, consult their documentation for similar settings.

## References
- [Apple Support: Resume feature](https://support.apple.com/en-us/HT202320)
- [iTerm2 Documentation](https://iterm2.com/documentation-preferences.html)

---

*This document is managed by the `terminal_setup` Ansible role.*
