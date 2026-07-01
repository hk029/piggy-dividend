import { View, Text } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useState, memo } from 'react'
import TabBar from '@/components/TabBar'
import './index.scss'

const CalendarPage = memo(() => {
  const [currentMonth] = useState({ year: 2025, month: 7 })

  return (
    <View className='calendar'>
      <View className='calendar__header'>
        <Text className='calendar__title'>攒息日历</Text>
      </View>

      <View className='calendar__month'>
        <Text className='calendar__month-arrow'>‹</Text>
        <Text className='calendar__month-text'>{currentMonth.year}年{currentMonth.month}月</Text>
        <Text className='calendar__month-arrow'>›</Text>
      </View>

      <View className='calendar__empty'>
        <View className='calendar__empty-piggy'>🐷📅</View>
        <Text className='calendar__empty-title'>日历还没有安排</Text>
        <Text className='calendar__empty-desc'>添加资产后，预计到账时间会在这里慢慢排开。</Text>
        <View className='calendar__empty-btn' onClick={() => Taro.redirectTo({ url: '/pages/asset/index' })}>
          <Text className='calendar__empty-btn-text'>去添加资产</Text>
        </View>
        <View className='calendar__empty-link'>
          <Text className='calendar__empty-link-text'>以后再来看</Text>
        </View>
      </View>

      <View className='calendar__summary'>
        <View className='calendar__summary-card'>
          <Text className='calendar__summary-icon'>📷</Text>
          <Text className='calendar__summary-label'>本月已收到（元）</Text>
          <Text className='calendar__summary-value'>—</Text>
        </View>
        <View className='calendar__summary-card'>
          <Text className='calendar__summary-icon'>🎁</Text>
          <Text className='calendar__summary-label'>本月还会收到（元）</Text>
          <Text className='calendar__summary-value'>—</Text>
        </View>
      </View>

      <TabBar active='calendar' />
    </View>
  )
})

export default CalendarPage
