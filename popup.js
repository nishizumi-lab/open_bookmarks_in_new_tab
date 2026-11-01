document.addEventListener("DOMContentLoaded", async () => {
  const enableToggle = document.getElementById("enable-toggle");
  const bgToggle = document.getElementById("bg-toggle");
  const searchInput = document.getElementById("search-input");
  const bookmarkList = document.getElementById("bookmark-list");

  // 保存されている設定の読み込み
  const config = await chrome.storage.sync.get({
    enabled: true,
    openInBackground: false
  });

  enableToggle.checked = config.enabled;
  bgToggle.checked = config.openInBackground;

  // 設定変更時の保存
  enableToggle.addEventListener("change", () => {
    chrome.storage.sync.set({ enabled: enableToggle.checked });
  });

  bgToggle.addEventListener("change", () => {
    chrome.storage.sync.set({ openInBackground: bgToggle.checked });
  });

  // ブックマーク一覧の取得・平坦化
  let allBookmarks = [];

  function flattenBookmarks(nodes) {
    for (const node of nodes) {
      if (node.url) {
        allBookmarks.push({
          title: node.title || node.url,
          url: node.url
        });
      }
      if (node.children) {
        flattenBookmarks(node.children);
      }
    }
  }

  const tree = await chrome.bookmarks.getTree();
  flattenBookmarks(tree);

  function renderList(bookmarks) {
    bookmarkList.innerHTML = "";
    if (bookmarks.length === 0) {
      const emptyDiv = document.createElement("div");
      emptyDiv.className = "bookmark-item";
      emptyDiv.textContent = "ブックマークが見つかりません";
      bookmarkList.appendChild(emptyDiv);
      return;
    }

    bookmarks.slice(0, 50).forEach((bm) => {
      const a = document.createElement("a");
      a.className = "bookmark-item";
      a.textContent = bm.title;
      a.title = bm.url;
      a.href = bm.url;
      a.addEventListener("click", async (e) => {
        e.preventDefault();
        const settings = await chrome.storage.sync.get({ openInBackground: false });
        await chrome.tabs.create({
          url: bm.url,
          active: !settings.openInBackground
        });
      });
      bookmarkList.appendChild(a);
    });
  }

  renderList(allBookmarks);

  // 検索フィルタ
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase().trim();
    if (!query) {
      renderList(allBookmarks);
      return;
    }
    const filtered = allBookmarks.filter((bm) => {
      return (
        bm.title.toLowerCase().includes(query) ||
        bm.url.toLowerCase().includes(query)
      );
    });
    renderList(filtered);
  });
});
