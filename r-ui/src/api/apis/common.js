import { request } from '@/utils/request.js'


export default {

    /**
     * 获取用户列表
     * @returns
     */
    getUserList (params = {}) {
        return request({
            url: 'admin/user/getUserList',
            method: 'get',
            params
        })
    },

    /**
     * 获取部门列表
     * @returns
     */
    getDeptTreeList (params = {}) {
        return request({
            url: 'admin/user/getDeptTreeList',
            method: 'get',
            params
        })
    },

    /**
     * 获取角色列表
     * @returns
     */
    getRoleList (params = {}) {
        return request({
            url: 'admin/user/getRoleList',
            method: 'get',
            params
        })
    },

    /**
     * 获取岗位列表
     * @returns
     */
    getPostList (params = {}) {
        return request({
            url: 'admin/user/getPostList',
            method: 'get',
            params
        })
    },
}
