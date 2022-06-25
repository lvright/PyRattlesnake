<template>
	<el-card shadow="hover" header="欢迎">
		<div class="welcome">
			<div class="logo">
				<img src="img/logo.svg">
				<h2>响尾蛇 PyRattlesnake</h2>
			</div>
			<div class="tips">
				<div class="tips-item">
					<div class="tips-item-icon"><el-icon><el-icon-promotion /></el-icon></div>
					<div class="tips-item-message">PyRattlesnake 后端是基于FastAPI框架，是高性能、易于学习、高效编码的框架</div>
				</div>
				<div class="tips-item">
					<div class="tips-item-icon"><el-icon><el-icon-star /></el-icon></div>
					<div class="tips-item-message">PyRattlesnake的Vue是套用MineAdmin，MineAdmin是我认为比较精致美观的Vue后台框架</div>
				</div>
				<div class="tips-item">
					<div class="tips-item-icon"><el-icon><el-icon-coffee /></el-icon></div>
					<div class="tips-item-message">如果有想一起维护的蛇友请在gitee仓库上给我留言</div>
				</div>
			</div>
			<div class="actions">
				<el-button type="primary" icon="el-icon-check" @click="godoc">Github</el-button>
			</div>
		</div>
	</el-card>
</template>

<script>
	export default {
		title: "欢迎",
		icon: "el-icon-present",
		description: "项目特色以及文档链接",
		data() {
			return {

			}
		},
		methods: {
			godoc(){
				window.open("https://github.com/lvright/PyRattlesnake")
			}
		}
	}
</script>

<style scoped>
	.welcome {}
	.welcome .logo {text-align: center;}
	.welcome .logo img {vertical-align: bottom;width: 100px;height: 100px;margin-bottom: 20px;}
	.welcome .logo h2 {font-size: 30px;font-weight: normal;display: flex;align-items: center;justify-content: center;}

	.tips {margin-top: 20px;padding:0 40px;}
	.tips-item {display: flex;align-items: center;justify-content: center;padding:7.5px 0;}
	.tips-item-icon {width: 40px;height:40px;display: flex;align-items: center;justify-content: center;border-radius: 50%;font-size: 18px;margin-right: 20px;color: var(--el-color-primary);background: rgba(180,180,180,0.1);}
	.tips-item-message {flex: 1;font-size: 14px;}

	.actions {text-align: center;margin: 40px 0 20px 0;}
</style>
