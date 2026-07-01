import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useState, memo } from 'react'
import TabBar from '@/components/TabBar'
import './index.scss'

type TabType = 'all' | 'received' | 'pending'

const LedgerPage = memo(() => {
  const [activeTab, setActiveTab] = useState<TabType>('all')

  const tabs: { key: TabType; label: string }[] = [
    { key: 'all', label: '全部' },
    { key: 'received', label: '已到账' },
    { key: 'pending', label: '待到账' },
  ]

  return (
    <View className='ledger'>
      <View className='ledger__header'>
        <Text className='ledger__title'>分红账本</Text>
      </View>

      <View className='ledger__tabs'>
        {tabs.map(tab => (
          <View 
            key={tab.key}
            className={`ledger__tab ${activeTab === tab.key ? 'ledger__tab--active' : ''}`}
            onClick={() => setActiveTab(tab.key)}
          >
            <Text className='ledger__tab-text'>{tab.label}</Text>
          </View>
        ))}
      </View>

      <View className='ledger__empty'>
        <View className='ledger__empty-piggy'>🐷📖</View>
        <Text className='ledger__empty-title'>还没有分红记录</Text>
        <Text className='ledger__empty-desc'>等第一笔分红到账，这里会帮你记成清清楚楚的攒息账本。</Text>
        <View className='ledger__empty-btn' onClick={() => Taro.redirectTo({ url: '/pages/asset/index' })}>
          <Text className='ledger__empty-btn-text'>去添加资产</Text>
        </View>
        <View className='ledger__empty-link' onClick={() => Taro.redirectTo({ url: '/pages/calendar/index' })}>
          <Text className='ledger__empty-link-text'>先看看攒息日历</Text>
          <Text className='ledger__empty-link-arrow'>›</Text>
        </View>
      </View>

      <View className='ledger__summary'>
        <View className='ledger__summary-card'>
          <Text className='ledger__summary-icon'>📷</Text>
          <Text className='ledger__summary-label'>本月已收（元）</Text>
          <Text className='ledger__summary-value'>—</Text>
          <Text className='ledger__summary-compare'>较上月 —</Text>
        </View>
        <View className='ledger__summary-card'>
          <Text className='ledger__summary-icon'>⏰</Text>
          <Text className='ledger__summary-label'>待到账（元）</Text>
          <Text className='ledger__summary-value'>—</Text>
          <Text className='ledger__summary-compare'>较上月 —</Text>
        </View>
      </View>

      <TabBar active='ledger' />
    </View>
  )
})

export default LedgerPage
