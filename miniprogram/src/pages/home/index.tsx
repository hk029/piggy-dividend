import { View, Text, Image } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { memo } from 'react'
import './index.scss'

const HomePage = memo(() => {
  return (
    <View className='home'>
      <View className='home__header'>
        <Text className='home__title'>小猪攒息</Text>
        <View className='home__notice'>
          <Text className='home__notice-icon'>🔔</Text>
        </View>
      </View>

      <View className='home__empty'>
        <Image className='home__empty-img' src='/assets/images/empty-home.png' mode='aspectFit' />
        <Text className='home__empty-title'>还没开始攒息</Text>
        <Text className='home__empty-desc'>添加第一笔资产后，小猪会帮你慢慢攒起每一笔分红。</Text>
        <View className='home__empty-btn' onClick={() => Taro.switchTab({ url: '/pages/asset/index' })}>
          <Text className='home__empty-btn-text'>添加第一笔资产</Text>
        </View>
        <View className='home__empty-link' onClick={() => Taro.switchTab({ url: '/pages/asset/index' })}>
          <Text className='home__empty-link-text'>先去看看关注资产</Text>
          <Text className='home__empty-link-arrow'>›</Text>
        </View>
      </View>

      <View className='home__stats'>
        <View className='home__stat-item'>
          <Image className='home__stat-icon' src='/assets/images/bills.png' mode='aspectFit' />
          <Text className='home__stat-label'>今年已攒（元）</Text>
          <Text className='home__stat-value'>—</Text>
          <Text className='home__stat-compare'>较去年 —</Text>
        </View>
        <View className='home__stat-item'>
          <Image className='home__stat-icon' src='/assets/images/gift.png' mode='aspectFit' />
          <Text className='home__stat-label'>本月累计分红</Text>
          <Text className='home__stat-value'>—</Text>
          <Text className='home__stat-compare'>较上月 —</Text>
        </View>
        <View className='home__stat-item'>
          <Image className='home__stat-icon' src='/assets/images/qianbao.png' mode='aspectFit' />
          <Text className='home__stat-label'>分红笔数</Text>
          <Text className='home__stat-count'>0</Text>
          <Text className='home__stat-compare'>较上月 +0</Text>
        </View>
      </View>
    </View>
  )
})

export default HomePage
