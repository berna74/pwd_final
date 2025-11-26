const articulos_routes = [
    {
        path: '/articulos',
        component: ()=>import('../views/ArticulosView.vue'),
        children: [
            {
                path: '',
                name: 'articulos_list',
                component: ()=>import('../components/articulos/ArticulosList.vue')
            },
            {
                path: ':id/show',
                name: 'articulos_show',
                component: ()=>import('../components/articulos/ArticulosShow.vue')
            },
            {
                path: 'create',
                name: 'articulos_create',
                component: ()=>import('../components/articulos/ArticulosCreate.vue')
            },
            {
                path: ':id/edit',
                name: 'articulos_edit',
                component: ()=>import('../components/articulos/ArticulosUpdate.vue')
            }
        ]
    }
]
export default articulos_routes