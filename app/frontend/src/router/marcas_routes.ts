const marcas_routes = [
    {
        path: '/marcas',
        component: ()=>import('../views/MarcasView.vue'),
        children: [
            {
                path: '',
                name: 'marcas_list',
                component: ()=>import('../components/marcas/MarcasList.vue')
            },
            {
                path: ':id/show',
                name: 'marcas_show',
                component: ()=>import('../components/marcas/MarcasShow.vue')
            },
            {
                path: 'create',
                name: 'marcas_create',
                component: ()=>import('../components/marcas/MarcasCreate.vue')
            },
            {
                path: ':id/edit',
                name: 'marcas_edit',
                component: ()=>import('../components/marcas/MarcasUpdate.vue')
            }
        ]
    }
]
export default marcas_routes