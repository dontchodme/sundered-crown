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
});
