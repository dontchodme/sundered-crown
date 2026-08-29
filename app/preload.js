/* The ONLY surface the page can reach. Everything here is a named capability;
 * nothing generic is exposed. If a future phase needs the filesystem, it gets
 * a named function for the one thing it needs, not `fs`. */
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('swb', {
  gamePath:      () => ipcRenderer.invoke('swb:gamePath'),
  repoRoot:      () => ipcRenderer.invoke('swb:repoRoot'),
  writeIdentity: (payload) => ipcRenderer.invoke('swb:writeIdentity', payload),
  revealFile:    (p) => ipcRenderer.invoke('swb:revealFile', p),
  createShort:   (opts) => ipcRenderer.invoke('swb:createShort', opts),
  speak:         (opts) => ipcRenderer.invoke('swb:speak', opts),
  voices:        () => ipcRenderer.invoke('swb:voices'),
  hookScript:    (opts) => ipcRenderer.invoke('swb:hookScript', opts),
  cancelShort:   () => ipcRenderer.invoke('swb:cancelShort'),
  /* PUSH, not poll. A capture is minutes long and says something once a
   * second; asking for its state on a timer would be a second clock to keep
   * in step with the first. Listener-only -- the page can receive on these
   * channels and cannot send on them. */
  onShortProgress: (fn) => ipcRenderer.on('swb:shortProgress', (_e, d) => fn(d)),
  onShortLog:      (fn) => ipcRenderer.on('swb:shortLog', (_e, d) => fn(d)),
  onShortDone:     (fn) => ipcRenderer.on('swb:shortDone', (_e, d) => fn(d)),
});
