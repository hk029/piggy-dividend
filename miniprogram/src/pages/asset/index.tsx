import { View, Text, Image } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { useState, memo } from 'react'
import './index.scss'

type AssetTab = 'mine' | 'watch'

const AssetPage = memo(() => {
  const [activeTab, setActiveTab] = useState<AssetTab>('mine')

  return (
    <View className='asset'>
      <View className='asset__header'>
        <Text className='asset__title'>资产</Text>
      </View>

      <View className='asset__tabs'>
        <View 
          className={`asset__tab ${activeTab === 'mine' ? 'asset__tab--active' : ''}`}
          onClick={() => setActiveTab('mine')}
        >
          <Text className='asset__tab-text'>我的资产</Text>
        </View>
        <View 
          className={`asset__tab ${activeTab === 'watch' ? 'asset__tab--active' : ''}`}
          onClick={() => setActiveTab('watch')}
        >
          <Text className='asset__tab-text'>关注资产</Text>
        </View>
      </View>

      {activeTab === 'mine' && (
        <View className='asset__empty'>
          <Image className='asset__empty-img' src='/assets/images/empty-asset.png' mode='aspectFit' />
          <Text className='asset__empty-title'>你还没有资产</Text>
          <Text className='asset__empty-desc'>添加持有资产后，可以看到我的平均股息率、下次预计到账和今年已攒息。</Text>
          <View className='asset__empty-btn'>
            <Text className='asset__empty-btn-text'>添加第一笔资产</Text>
          </View>
          <View className='asset__empty-link' onClick={() => setActiveTab('watch')}>
            <Text className='asset__empty-link-text'>切换到关注资产</Text>
            <Text className='asset__empty-link-arrow'>›</Text>
          </View>
        </View>
      )}

      {activeTab === 'watch' && (
        <View className='asset__empty'>
          <Image className='asset__empty-img' src='/assets/images/empty-asset.png' mode='aspectFit' />
          <Text className='asset__empty-title'>还没有关注资产</Text>
          <Text className='asset__empty-desc'>关注心仪的好资产，等合适时机一起攒息。</Text>
          <View className='asset__empty-btn'>
            <Text className='asset__empty-btn-text'>添加关注资产</Text>
          </View>
          <View className='asset__empty-link' onClick={() => setActiveTab('mine')}>
            <Text className='asset__empty-link-text'>切换到我的资产</Text>
            <Text className='asset__empty-link-arrow'>›</Text>
          </View>
        </View>
      )}

      <View className='asset__stats'>
        <View className='asset__stat-item'>
          <Text className='asset__stat-icon'>📊</Text>
          <Text className='asset__stat-label'>我的平均股息率</Text>
          <Text className='asset__stat-value'>—</Text>
          <Text className='asset__stat-unit'>%</Text>
        </View>
        <View className='asset__stat-item'>
          <Text className='asset__stat-icon'>📅</Text>
          <Text className='asset__stat-label'>下次预计到账</Text>
          <Text className='asset__stat-value'>—</Text>
          <Text className='asset__stat-unit'>—</Text>
        </View>
        <View className='asset__stat-item'>
          <Text className='asset__stat-icon'>🐷</Text>
          <Text className='asset__stat-label'>今年已攒息</Text>
          <Text className='asset__stat-value'>—</Text>
          <Text className='asset__stat-unit'>元</Text>
        </View>
      </View>
    </View>
  )
})

export default AssetPage
