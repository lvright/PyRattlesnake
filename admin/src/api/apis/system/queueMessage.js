import { request } from '@/utils/request.js'

export default {

    /**
     * 获取接收消息列表
     * @returns
     */
    getReceiveList (params = {}) {
        return request({
            url: 'admin/queueMessage/receiveList',
            method: 'get',
            params
        })
    },
  
    /**
     * 获取发送消息列表
     * @returns
     */
    getSendList (params = {}) {
        return request({
            url: 'admin/queueMessage/sendList',
            method: 'get',
            params
        })
    },

    /**
     * 获取接收人列表
     * @returns
     */
    getReceiveUser (params = {}) {
        return request({
            url: 'admin/queueMessage/getReceiveUser',
            method: 'get',
            params
        })
    },

    /**
     * 删除消息
     * @returns
     */
    deletes (ids) {
        return request({
            url: 'admin/queueMessage/delete/' + ids,
            method: 'delete'
        })
    },

    /**
     * 更新读取状态
     * @returns
     */
    updateReadStatus (id = {}) {
        return request({
            url: 'admin/queueMessage/readMessage/' + id,
            method: 'get',
        })
    },

    /**
     * 发私信
     * @returns
     */
    sendPrivateMessage (data = {}) {
        return request({
            url: 'admin/queueMessage/sendPrivateMessage',
            method: 'post',
            data
        })
    },
}