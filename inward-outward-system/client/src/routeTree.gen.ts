/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file was automatically generated by TanStack Router.
// You should NOT make any changes in this file as it will be overwritten.
// Additionally, you should also exclude this file from your linter and/or formatter to prevent it from being checked or modified.

// Import Routes

import { Route as rootRoute } from './routes/__root'
import { Route as ProtectedImport } from './routes/_protected'
import { Route as AuthImport } from './routes/_auth'
import { Route as ProtectedIndexImport } from './routes/_protected/index'
import { Route as ProtectedUsersImport } from './routes/_protected/users'
import { Route as ProtectedTurninImport } from './routes/_protected/turn_in'
import { Route as ProtectedStatsImport } from './routes/_protected/stats'
import { Route as ProtectedOtherapplicationImport } from './routes/_protected/other_application'
import { Route as ProtectedHandinImport } from './routes/_protected/hand_in'
import { Route as AuthSignupImport } from './routes/_auth/signup'
import { Route as AuthLoginImport } from './routes/_auth/login'
import { Route as ProtectedUserIdImport } from './routes/_protected/user.$id'
import { Route as ProtectedUpdateIdImport } from './routes/_protected/update.$id'
import { Route as ProtectedForwardIdImport } from './routes/_protected/forward.$id'
import { Route as ProtectedApplicationIdImport } from './routes/_protected/application.$id'
import { Route as AuthVerifyTokenImport } from './routes/_auth/verify.$token'

// Create/Update Routes

const ProtectedRoute = ProtectedImport.update({
  id: '/_protected',
  getParentRoute: () => rootRoute,
} as any)

const AuthRoute = AuthImport.update({
  id: '/_auth',
  getParentRoute: () => rootRoute,
} as any)

const ProtectedIndexRoute = ProtectedIndexImport.update({
  id: '/',
  path: '/',
  getParentRoute: () => ProtectedRoute,
} as any)

const ProtectedUsersRoute = ProtectedUsersImport.update({
  id: '/users',
  path: '/users',
  getParentRoute: () => ProtectedRoute,
} as any)

const ProtectedTurninRoute = ProtectedTurninImport.update({
  id: '/turn_in',
  path: '/turn_in',
  getParentRoute: () => ProtectedRoute,
} as any)

const ProtectedStatsRoute = ProtectedStatsImport.update({
  id: '/stats',
  path: '/stats',
  getParentRoute: () => ProtectedRoute,
} as any)

const ProtectedOtherapplicationRoute = ProtectedOtherapplicationImport.update({
  id: '/other_application',
  path: '/other_application',
  getParentRoute: () => ProtectedRoute,
} as any)

const ProtectedHandinRoute = ProtectedHandinImport.update({
  id: '/hand_in',
  path: '/hand_in',
  getParentRoute: () => ProtectedRoute,
} as any)

const AuthSignupRoute = AuthSignupImport.update({
  id: '/signup',
  path: '/signup',
  getParentRoute: () => AuthRoute,
} as any)

const AuthLoginRoute = AuthLoginImport.update({
  id: '/login',
  path: '/login',
  getParentRoute: () => AuthRoute,
} as any)

const ProtectedUserIdRoute = ProtectedUserIdImport.update({
  id: '/user/$id',
  path: '/user/$id',
  getParentRoute: () => ProtectedRoute,
} as any)

const ProtectedUpdateIdRoute = ProtectedUpdateIdImport.update({
  id: '/update/$id',
  path: '/update/$id',
  getParentRoute: () => ProtectedRoute,
} as any)

const ProtectedForwardIdRoute = ProtectedForwardIdImport.update({
  id: '/forward/$id',
  path: '/forward/$id',
  getParentRoute: () => ProtectedRoute,
} as any)

const ProtectedApplicationIdRoute = ProtectedApplicationIdImport.update({
  id: '/application/$id',
  path: '/application/$id',
  getParentRoute: () => ProtectedRoute,
} as any)

const AuthVerifyTokenRoute = AuthVerifyTokenImport.update({
  id: '/verify/$token',
  path: '/verify/$token',
  getParentRoute: () => AuthRoute,
} as any)

// Populate the FileRoutesByPath interface

declare module '@tanstack/react-router' {
  interface FileRoutesByPath {
    '/_auth': {
      id: '/_auth'
      path: ''
      fullPath: ''
      preLoaderRoute: typeof AuthImport
      parentRoute: typeof rootRoute
    }
    '/_protected': {
      id: '/_protected'
      path: ''
      fullPath: ''
      preLoaderRoute: typeof ProtectedImport
      parentRoute: typeof rootRoute
    }
    '/_auth/login': {
      id: '/_auth/login'
      path: '/login'
      fullPath: '/login'
      preLoaderRoute: typeof AuthLoginImport
      parentRoute: typeof AuthImport
    }
    '/_auth/signup': {
      id: '/_auth/signup'
      path: '/signup'
      fullPath: '/signup'
      preLoaderRoute: typeof AuthSignupImport
      parentRoute: typeof AuthImport
    }
    '/_protected/hand_in': {
      id: '/_protected/hand_in'
      path: '/hand_in'
      fullPath: '/hand_in'
      preLoaderRoute: typeof ProtectedHandinImport
      parentRoute: typeof ProtectedImport
    }
    '/_protected/other_application': {
      id: '/_protected/other_application'
      path: '/other_application'
      fullPath: '/other_application'
      preLoaderRoute: typeof ProtectedOtherapplicationImport
      parentRoute: typeof ProtectedImport
    }
    '/_protected/stats': {
      id: '/_protected/stats'
      path: '/stats'
      fullPath: '/stats'
      preLoaderRoute: typeof ProtectedStatsImport
      parentRoute: typeof ProtectedImport
    }
    '/_protected/turn_in': {
      id: '/_protected/turn_in'
      path: '/turn_in'
      fullPath: '/turn_in'
      preLoaderRoute: typeof ProtectedTurninImport
      parentRoute: typeof ProtectedImport
    }
    '/_protected/users': {
      id: '/_protected/users'
      path: '/users'
      fullPath: '/users'
      preLoaderRoute: typeof ProtectedUsersImport
      parentRoute: typeof ProtectedImport
    }
    '/_protected/': {
      id: '/_protected/'
      path: '/'
      fullPath: '/'
      preLoaderRoute: typeof ProtectedIndexImport
      parentRoute: typeof ProtectedImport
    }
    '/_auth/verify/$token': {
      id: '/_auth/verify/$token'
      path: '/verify/$token'
      fullPath: '/verify/$token'
      preLoaderRoute: typeof AuthVerifyTokenImport
      parentRoute: typeof AuthImport
    }
    '/_protected/application/$id': {
      id: '/_protected/application/$id'
      path: '/application/$id'
      fullPath: '/application/$id'
      preLoaderRoute: typeof ProtectedApplicationIdImport
      parentRoute: typeof ProtectedImport
    }
    '/_protected/forward/$id': {
      id: '/_protected/forward/$id'
      path: '/forward/$id'
      fullPath: '/forward/$id'
      preLoaderRoute: typeof ProtectedForwardIdImport
      parentRoute: typeof ProtectedImport
    }
    '/_protected/update/$id': {
      id: '/_protected/update/$id'
      path: '/update/$id'
      fullPath: '/update/$id'
      preLoaderRoute: typeof ProtectedUpdateIdImport
      parentRoute: typeof ProtectedImport
    }
    '/_protected/user/$id': {
      id: '/_protected/user/$id'
      path: '/user/$id'
      fullPath: '/user/$id'
      preLoaderRoute: typeof ProtectedUserIdImport
      parentRoute: typeof ProtectedImport
    }
  }
}

// Create and export the route tree

interface AuthRouteChildren {
  AuthLoginRoute: typeof AuthLoginRoute
  AuthSignupRoute: typeof AuthSignupRoute
  AuthVerifyTokenRoute: typeof AuthVerifyTokenRoute
}

const AuthRouteChildren: AuthRouteChildren = {
  AuthLoginRoute: AuthLoginRoute,
  AuthSignupRoute: AuthSignupRoute,
  AuthVerifyTokenRoute: AuthVerifyTokenRoute,
}

const AuthRouteWithChildren = AuthRoute._addFileChildren(AuthRouteChildren)

interface ProtectedRouteChildren {
  ProtectedHandinRoute: typeof ProtectedHandinRoute
  ProtectedOtherapplicationRoute: typeof ProtectedOtherapplicationRoute
  ProtectedStatsRoute: typeof ProtectedStatsRoute
  ProtectedTurninRoute: typeof ProtectedTurninRoute
  ProtectedUsersRoute: typeof ProtectedUsersRoute
  ProtectedIndexRoute: typeof ProtectedIndexRoute
  ProtectedApplicationIdRoute: typeof ProtectedApplicationIdRoute
  ProtectedForwardIdRoute: typeof ProtectedForwardIdRoute
  ProtectedUpdateIdRoute: typeof ProtectedUpdateIdRoute
  ProtectedUserIdRoute: typeof ProtectedUserIdRoute
}

const ProtectedRouteChildren: ProtectedRouteChildren = {
  ProtectedHandinRoute: ProtectedHandinRoute,
  ProtectedOtherapplicationRoute: ProtectedOtherapplicationRoute,
  ProtectedStatsRoute: ProtectedStatsRoute,
  ProtectedTurninRoute: ProtectedTurninRoute,
  ProtectedUsersRoute: ProtectedUsersRoute,
  ProtectedIndexRoute: ProtectedIndexRoute,
  ProtectedApplicationIdRoute: ProtectedApplicationIdRoute,
  ProtectedForwardIdRoute: ProtectedForwardIdRoute,
  ProtectedUpdateIdRoute: ProtectedUpdateIdRoute,
  ProtectedUserIdRoute: ProtectedUserIdRoute,
}

const ProtectedRouteWithChildren = ProtectedRoute._addFileChildren(
  ProtectedRouteChildren,
)

export interface FileRoutesByFullPath {
  '': typeof ProtectedRouteWithChildren
  '/login': typeof AuthLoginRoute
  '/signup': typeof AuthSignupRoute
  '/hand_in': typeof ProtectedHandinRoute
  '/other_application': typeof ProtectedOtherapplicationRoute
  '/stats': typeof ProtectedStatsRoute
  '/turn_in': typeof ProtectedTurninRoute
  '/users': typeof ProtectedUsersRoute
  '/': typeof ProtectedIndexRoute
  '/verify/$token': typeof AuthVerifyTokenRoute
  '/application/$id': typeof ProtectedApplicationIdRoute
  '/forward/$id': typeof ProtectedForwardIdRoute
  '/update/$id': typeof ProtectedUpdateIdRoute
  '/user/$id': typeof ProtectedUserIdRoute
}

export interface FileRoutesByTo {
  '': typeof AuthRouteWithChildren
  '/login': typeof AuthLoginRoute
  '/signup': typeof AuthSignupRoute
  '/hand_in': typeof ProtectedHandinRoute
  '/other_application': typeof ProtectedOtherapplicationRoute
  '/stats': typeof ProtectedStatsRoute
  '/turn_in': typeof ProtectedTurninRoute
  '/users': typeof ProtectedUsersRoute
  '/': typeof ProtectedIndexRoute
  '/verify/$token': typeof AuthVerifyTokenRoute
  '/application/$id': typeof ProtectedApplicationIdRoute
  '/forward/$id': typeof ProtectedForwardIdRoute
  '/update/$id': typeof ProtectedUpdateIdRoute
  '/user/$id': typeof ProtectedUserIdRoute
}

export interface FileRoutesById {
  __root__: typeof rootRoute
  '/_auth': typeof AuthRouteWithChildren
  '/_protected': typeof ProtectedRouteWithChildren
  '/_auth/login': typeof AuthLoginRoute
  '/_auth/signup': typeof AuthSignupRoute
  '/_protected/hand_in': typeof ProtectedHandinRoute
  '/_protected/other_application': typeof ProtectedOtherapplicationRoute
  '/_protected/stats': typeof ProtectedStatsRoute
  '/_protected/turn_in': typeof ProtectedTurninRoute
  '/_protected/users': typeof ProtectedUsersRoute
  '/_protected/': typeof ProtectedIndexRoute
  '/_auth/verify/$token': typeof AuthVerifyTokenRoute
  '/_protected/application/$id': typeof ProtectedApplicationIdRoute
  '/_protected/forward/$id': typeof ProtectedForwardIdRoute
  '/_protected/update/$id': typeof ProtectedUpdateIdRoute
  '/_protected/user/$id': typeof ProtectedUserIdRoute
}

export interface FileRouteTypes {
  fileRoutesByFullPath: FileRoutesByFullPath
  fullPaths:
    | ''
    | '/login'
    | '/signup'
    | '/hand_in'
    | '/other_application'
    | '/stats'
    | '/turn_in'
    | '/users'
    | '/'
    | '/verify/$token'
    | '/application/$id'
    | '/forward/$id'
    | '/update/$id'
    | '/user/$id'
  fileRoutesByTo: FileRoutesByTo
  to:
    | ''
    | '/login'
    | '/signup'
    | '/hand_in'
    | '/other_application'
    | '/stats'
    | '/turn_in'
    | '/users'
    | '/'
    | '/verify/$token'
    | '/application/$id'
    | '/forward/$id'
    | '/update/$id'
    | '/user/$id'
  id:
    | '__root__'
    | '/_auth'
    | '/_protected'
    | '/_auth/login'
    | '/_auth/signup'
    | '/_protected/hand_in'
    | '/_protected/other_application'
    | '/_protected/stats'
    | '/_protected/turn_in'
    | '/_protected/users'
    | '/_protected/'
    | '/_auth/verify/$token'
    | '/_protected/application/$id'
    | '/_protected/forward/$id'
    | '/_protected/update/$id'
    | '/_protected/user/$id'
  fileRoutesById: FileRoutesById
}

export interface RootRouteChildren {
  AuthRoute: typeof AuthRouteWithChildren
  ProtectedRoute: typeof ProtectedRouteWithChildren
}

const rootRouteChildren: RootRouteChildren = {
  AuthRoute: AuthRouteWithChildren,
  ProtectedRoute: ProtectedRouteWithChildren,
}

export const routeTree = rootRoute
  ._addFileChildren(rootRouteChildren)
  ._addFileTypes<FileRouteTypes>()

/* ROUTE_MANIFEST_START
{
  "routes": {
    "__root__": {
      "filePath": "__root.tsx",
      "children": [
        "/_auth",
        "/_protected"
      ]
    },
    "/_auth": {
      "filePath": "_auth.tsx",
      "children": [
        "/_auth/login",
        "/_auth/signup",
        "/_auth/verify/$token"
      ]
    },
    "/_protected": {
      "filePath": "_protected.tsx",
      "children": [
        "/_protected/hand_in",
        "/_protected/other_application",
        "/_protected/stats",
        "/_protected/turn_in",
        "/_protected/users",
        "/_protected/",
        "/_protected/application/$id",
        "/_protected/forward/$id",
        "/_protected/update/$id",
        "/_protected/user/$id"
      ]
    },
    "/_auth/login": {
      "filePath": "_auth/login.tsx",
      "parent": "/_auth"
    },
    "/_auth/signup": {
      "filePath": "_auth/signup.tsx",
      "parent": "/_auth"
    },
    "/_protected/hand_in": {
      "filePath": "_protected/hand_in.tsx",
      "parent": "/_protected"
    },
    "/_protected/other_application": {
      "filePath": "_protected/other_application.tsx",
      "parent": "/_protected"
    },
    "/_protected/stats": {
      "filePath": "_protected/stats.tsx",
      "parent": "/_protected"
    },
    "/_protected/turn_in": {
      "filePath": "_protected/turn_in.tsx",
      "parent": "/_protected"
    },
    "/_protected/users": {
      "filePath": "_protected/users.tsx",
      "parent": "/_protected"
    },
    "/_protected/": {
      "filePath": "_protected/index.tsx",
      "parent": "/_protected"
    },
    "/_auth/verify/$token": {
      "filePath": "_auth/verify.$token.tsx",
      "parent": "/_auth"
    },
    "/_protected/application/$id": {
      "filePath": "_protected/application.$id.tsx",
      "parent": "/_protected"
    },
    "/_protected/forward/$id": {
      "filePath": "_protected/forward.$id.tsx",
      "parent": "/_protected"
    },
    "/_protected/update/$id": {
      "filePath": "_protected/update.$id.tsx",
      "parent": "/_protected"
    },
    "/_protected/user/$id": {
      "filePath": "_protected/user.$id.tsx",
      "parent": "/_protected"
    }
  }
}
ROUTE_MANIFEST_END */
