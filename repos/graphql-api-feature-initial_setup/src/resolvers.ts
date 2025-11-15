import { mergeResolvers } from '@graphql-tools/merge'
import { resolvers as workflow } from './workflow/resolvers.js';
import { resolvers as fub } from './fub/resolvers.js';
import { resolvers as opp } from './opp/resolver.js';


export const resolvers = mergeResolvers([workflow, fub, opp])
