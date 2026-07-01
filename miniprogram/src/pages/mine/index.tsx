import { View, Text, Switch } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useState, memo } from 'react'
import TabBar from '@/components/TabBar'
import './index.scss'

const MinePage = memo(() => {
  const [privacyMode, setPrivacyMode] = useState(true)
  const [showAmount, setShowAmount] = useState(true)

  const menuItems = [
    { title: '隐私设置', icon: '🔒', arrow: true },
    { title: '金额显示', icon: '💰', arrow: true },
    { title: '分红规则', icon: '📋', arrow: true },
    { title: '数据口径', icon: '📊', arrow: true },
    { title: '提醒偏好', icon: '🔔', arrow: true },
    { title: '关于我们', icon: '🐷', arrow: true },
  ]

  return (
    <View className='mine'>
      <View className='mine__header'>
        <Text className='mine__title'>我的</Text>
      </View>

      <View className='mine__user'>
        <View className='mine__avatar'>
          <Text className='mine__avatar-text'>🐷</Text>
        </View>
        <View className='mine__user-info'>
          <Text className='mine__user-name'>小猪攒息用户</Text>
          <Text className='mine__user-id'>ID: 100001</Text>
        </View>
      </View>

      <View className='mine__settings'>
        <View className='mine__setting-item'>
          <Text className='mine__setting-label'>隐私模式</Text>
          <Switch 
            checked={privacyMode} 
            color='#2F5A42'
            onChange={(e) => setPrivacyMode(e.detail.value)}
          />
        </View>
        <View className='mine__setting-item'>
          <Text className='mine__setting-label'>金额显示</Text>
          <Switch 
            checked={showAmount} 
            color='#2F5A42'
            onChange={(e) => setShowAmount(e.detail.value)}
          />
        </View>
      </View>

      <View className='mine__menu'>
        {menuItems.map((item, index) => (
          <View 
            key={index} 
            className='mine__menu-item'
            onClick={() => Taro.showToast({ title: item.title, icon: 'none' })}
          >
            <Text className='mine__menu-icon'>{item.icon}</Text>
            <Text className='mine__menu-text'>{item.title}</Text>
            {item.arrow && <Text className='mine__menu-arrow'>›</Text>}
          </View>
        ))}
      </View>

      <View className='mine__version'>
        <Text className='mine__version-text'>小猪攒息 v1.0.0</Text>
      </View>

      <TabBar active='mine' />
    </View>
  )
})

export default MinePage
