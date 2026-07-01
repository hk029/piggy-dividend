import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { memo } from 'react'
import './index.scss'

type TabKey = 'home' | 'ledger' | 'calendar' | 'asset' | 'mine'

interface TabItem {
  key: TabKey
  label: string
  icon: string
  activeIcon: string
  path: string
}

const tabs: TabItem[] = [
  { key: 'home', label: '首页', icon: '🏠', activeIcon: '🏡', path: '/pages/home/index' },
  { key: 'ledger', label: '账本', icon: '📒', activeIcon: '📕', path: '/pages/ledger/index' },
  { key: 'calendar', label: '日历', icon: '📅', activeIcon: '📆', path: '/pages/calendar/index' },
  { key: 'asset', label: '资产', icon: '💰', activeIcon: '💎', path: '/pages/asset/index' },
  { key: 'mine', label: '我的', icon: '👤', activeIcon: '🐷', path: '/pages/mine/index' },
]

interface TabBarProps {
  active: TabKey
}

const TabBar = memo(({ active }: TabBarProps) => {
  const handleTabClick = (tab: TabItem) => {
    if (tab.key === active) return
    Taro.redirectTo({ url: tab.path })
  }

  return (
    <View className='tabbar'>
      {tabs.map(tab => (
        <View 
          key={tab.key}
          className={`tabbar__item ${tab.key === active ? 'tabbar__item--active' : ''}`}
          onClick={() => handleTabClick(tab)}
        >
          <Text className='tabbar__icon'>{tab.key === active ? tab.activeIcon : tab.icon}</Text>
          <Text className='tabbar__label'>{tab.label}</Text>
        </View>
      ))}
    </View>
  )
})

export default TabBar
export type { TabKey }
