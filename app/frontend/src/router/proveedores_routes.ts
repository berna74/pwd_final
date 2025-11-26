const proveedores_routes = [
    {
        path: '/proveedores',
        component: ()=>import('../views/ProveedoresView.vue'),
        children: [
            {
                path: '',
                name: 'proveedores_list',
                component: ()=>import('../components/proveedores/ProveedoresList.vue')
            },
            {
                path: ':id/show',
                name: 'proveedores_show',
                component: ()=>import('../components/proveedores/ProveedoresShow.vue')
            },
            {
                path: 'create',
                name: 'proveedores_create',
                component: ()=>import('../components/proveedores/ProveedoresCreate.vue')
            },
            {
                path: ':id/edit',
                name: 'proveedores_edit',
                component: ()=>import('../components/proveedores/ProveedoresUpdate.vue')
            }
        ]
    }
]
export default proveedores_routes