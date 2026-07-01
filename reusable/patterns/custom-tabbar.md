# 自定义 TabBar 踩坑

## 问题背景

微信小程序原生 `tabBar` 最多只能配置 5 个 tab，但产品需要 6 个 tab（首页、账本、日历、目标、资产、我的）。

## 解决方案

使用自定义组件实现 TabBar，不使用原生 tabBar 配置。

## 关键踩坑

### 1. 移除原生 tabBar 配置

```typescript
// app.config.ts - 不要配置 tabBar
export default defineAppConfig({
  pages: [
    'pages/home/index',
    'pages/ledger/index',
    // ... 其他页面
  ],
  // 不要写 tabBar 配置！
})
```

### 2. 页面跳转使用 redirectTo，不要用 switchTab

**错误写法：**
```typescript
// ❌ 会报错：switchTab:fail can not switch to no-tabBar page
Taro.switchTab({ url: '/pages/ledger/index' })
```

**正确写法：**
```typescript
// ✅ 自定义 tabbar 页面间跳转用 reLaunch（推荐）或 redirectTo
Taro.reLaunch({ url: '/pages/ledger/index' })
```

### 3. 为什么用 redirectTo 而不是 navigateTo

- `navigateTo` 会保留当前页面，导致页面栈越来越深
- `redirectTo` 会关闭当前页面再打开新页面，适合 tab 间切换
- 自定义 tabbar 的每个页面都是独立的，不需要保留历史

### 4. TabBar 组件实现要点

```tsx
// components/TabBar/index.tsx
const TabBar = ({ active }: { active: TabKey }) => {
  const handleTabClick = (tab: TabItem) => {
    if (tab.key === active) return
    Taro.redirectTo({ url: tab.path })  // 用 redirectTo！
  }
  // ...
}
```

### 5. 页面底部留白

每个使用自定义 TabBar 的页面，底部需要留出 TabBar 的高度（通常 120rpx + safe-area）：

```scss
.page {
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}
```

## 总结

| 场景 | 正确做法 |
|------|----------|
| 原生 tabBar 页面跳转 | `Taro.switchTab()` |
| 自定义 tabBar 页面跳转 | `Taro.reLaunch()` 或 `Taro.redirectTo()` |
| 非 tab 页跳转到 tab 页 | `Taro.reLaunch()` |
| 普通页面间跳转 | `Taro.navigateTo()` |
