const tabUrlHistory = new Map();
const isProcessing = new Set();

// タブの更新時に直前のURLを追跡
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    tabUrlHistory.set(tabId, tab.url);
  }
});

// ナビゲーション開始時にも直前のURLを補足
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  if (details.frameId !== 0) return;
  try {
    const tab = await chrome.tabs.get(details.tabId);
    if (tab && tab.url) {
      tabUrlHistory.set(details.tabId, tab.url);
    }
  } catch (error) {
    // タブが存在しない場合は無視
  }
});

// ブックマークからの遷移（auto_bookmark）を検知
chrome.webNavigation.onCommitted.addListener(async (details) => {
  if (details.frameId !== 0) return;
  if (details.transitionType !== "auto_bookmark") return;

  // 連続処理の防止
  if (isProcessing.has(details.tabId)) return;
  isProcessing.add(details.tabId);

  try {
    const config = await chrome.storage.sync.get({
      enabled: true,
      openInBackground: false
    });

    if (!config.enabled) {
      return;
    }

    const prevUrl = tabUrlHistory.get(details.tabId) || "";

    // 空白タブまたは新規タブ判定
    const isNewTab =
      !prevUrl ||
      prevUrl === "chrome://newtab/" ||
      prevUrl === "about:blank" ||
      prevUrl.startsWith("chrome-search://") ||
      prevUrl.startsWith("chrome://new-tab-page");

    // 空白タブでのブックマーククリック時はそのまま遷移させる
    if (isNewTab) {
      tabUrlHistory.set(details.tabId, details.url);
      return;
    }

    // 元のタブの現在位置を取得
    const currentTab = await chrome.tabs.get(details.tabId);
    const newTabIndex = currentTab ? currentTab.index + 1 : undefined;

    // 新規タブでブックマークを開く
    await chrome.tabs.create({
      url: details.url,
      active: !config.openInBackground,
      index: newTabIndex
    });

    // 元のタブを直前のページへ戻す
    try {
      await chrome.tabs.goBack(details.tabId);
    } catch (backError) {
      if (prevUrl) {
        await chrome.tabs.update(details.tabId, { url: prevUrl });
      }
    }
  } catch (error) {
    console.error("ブックマーク処理エラー:", error);
  } finally {
    setTimeout(() => {
      isProcessing.delete(details.tabId);
    }, 500);
  }
});

// タブが閉じられた際の履歴クリーンアップ
chrome.tabs.onRemoved.addListener((tabId) => {
  tabUrlHistory.delete(tabId);
  isProcessing.delete(tabId);
});
