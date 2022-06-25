import { request } from '@/utils/request.js'

export default {

  /**
   * 获取服务器信息
   * @returns
   */
  getServerInfo () {
    return request({
      url: 'admin/config/server/monitor',
      method: 'get'
    })
  },

  /**
   * 获取在线用户列表
   * @param {*} params 
   * @returns 
   */
  getOnlineUserPageList (params = {}) {
    return request({
      url: 'admin/user/onlineUser/index',
      method: 'get',
      params
    })
  },

  /**
   * 强退用户 （踢下线）
   * @param {*} params 
   * @returns 
   */
  kickUser (params = {}) {
    return request({
      url: 'admin/user/onlineUser/kick',
      method: 'post',
      data: params
    })
  },

  /**
   * 获取缓存信息
   * @returns
   */
  getCacheInfo () {
    return request({
      url: 'admin/config/redis',
      method: 'get'
    })
  },

  /**
   * 查看key内容
   * @returns
   */
  view (data) {
    return request({
      url: 'admin/config/redisView',
      method: 'post',
      data
    })
  },
  

  /**
   * 删除一个缓存
   * @returns
   */
  deleteKey (data) {
    return request({
      url: 'admin/config/redisDelete',
      method: 'delete',
      data
    })
  },

  /**
   * 清空缓存
   * @returns
   */
  clear () {
    return request({
      url: 'admin/config/redisClear',
      method: 'delete'
    })
  },
}