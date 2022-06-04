import { request } from '@/utils/request.js'

export default {
    /**
     * 快捷查询字典
     * @returns
     * @param code
     */
    getDict(code) {
        return request({
            url: 'admin/config/apis/' + code,
            method: 'get'
        })
    },

    /**
     * 快捷查询多个字典
     * @returns
     * @param codes
     */
    getDicts(codes) {
        return request({
            url: 'system/dataDict/lists?codes=' + codes.join(','),
            method: 'get'
        })
    },

    /**
     * 获取字典数据分页列表
     * @returns
     */
    getPageList(params = {}) {
        return request({
            url: 'admin/config/dictDate',
            method: 'get',
            params
        })
    },

    /**
     * 从回收站获取字典数据
     * @returns
     */
    getRecyclePageList(params = {}) {
        return request({
            url: 'system/dataDict/recycle',
            method: 'get',
            params
        })
    },

    /**
     * 添加字典数据
     * @returns
     */
    saveDictData(params = {}) {
        return request({
            url: 'admin/config/dictDate/save',
            method: 'post',
            data: params
        })
    },

    /**
     * 移到回收站
     * @returns
     */
    deletesDictData(ids) {
        return request({
            url: 'admin/config/dictDate/delete/' + ids,
            method: 'delete'
        })
    },

    /**
     * 恢复数据
     * @returns
     */
    recoverysDictData(ids) {
        return request({
            url: 'system/dataDict/recovery/' + ids,
            method: 'put'
        })
    },

    /**
     * 真实删除
     * @returns
     */
    realDeletesDictData(ids) {
        return request({
            url: 'system/dataDict/realDelete/' + ids,
            method: 'delete'
        })
    },

    /**
     * 更新数据
     * @returns
     */
    updateDictData(id, params = {}) {
        return request({
            url: 'admin/config/dictDate/update/' + id,
            method: 'put',
            data: params
        })
    },

    /**
     * 清空缓存
     * @returns
     */
    clearCache() {
        return request({
            url: 'admin/config/dict/clearCache',
            method: 'post'
        })
    },

    /**
     * 更改字典状态
     * @returns
     */
    changeStatus (params = {}) {
        return request({
        url: 'admin/config/dict/changeStatus',
        method: 'put',
        data: params
        })
    },

}
