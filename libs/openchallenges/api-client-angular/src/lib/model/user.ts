/**
 * OpenChallenges API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
import { UserStatus } from './userStatus';


/**
 * A simple user
 */
export interface User { 
    /**
     * The unique identifier of an account
     */
    id?: number;
    login: string;
    /**
     * An email address.
     */
    email: string;
    name?: string | null;
    status?: UserStatus;
    avatarUrl?: string | null;
    createdAt: string;
    updatedAt: string;
    type: string;
    bio?: string | null;
}
