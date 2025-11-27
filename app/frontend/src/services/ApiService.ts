import {instance as axios} from '../plugins/axios';

class ApiService {
  // Métodos genéricos para los stores
  static async get(url: string) {
    try {
      const response = await axios.get(url);
      return response;
    } catch (error) {
      console.error('Error en GET:', error);
      throw error;
    }
  }

  static async post(url: string, data: object) {
    try {
      const response = await axios.post(url, data);
      return response;
    } catch (error) {
      console.error('Error en POST:', error);
      throw error;
    }
  }

  static async put(url: string, data: object) {
    try {
      const response = await axios.put(url, data);
      return response;
    } catch (error) {
      console.error('Error en PUT:', error);
      throw error;
    }
  }

  static async delete(url: string) {
    try {
      const response = await axios.delete(url);
      return response;
    } catch (error) {
      console.error('Error en DELETE:', error);
      throw error;
    }
  }

  // Métodos legacy
  static async getAll(url: string) {
    try {
      const response = await axios.get(`${url}/`);
      if (response) {
        return response.data;
      } 
    } catch (error) {
        return error
      }
  }

  static async getOne(url: string, id: number) {
  try {
      const response = await axios.get(`${url}/${id}`);
      if (response) {
        return response.data;
      } 
    } catch (error) {
        return error
      }
}


  static async create(url:string, data:object) {
  try {
    const response = await axios.post(`${url}/`, data)
    if (response) {
      return response.data;
    }
  } catch (error) {
    console.error('Error en create:', error);
    throw error;
  }
}


  static async update(url: string, id: number, data: object) {
  try {
    const response = await axios.put(`${url}/${id}`, data)
    if (response) {
      return response.data;
    }
  } catch (error) {
    return error;
  }
}

  static async destroy(url: string, id: number) {
  try {
    const response = await axios.delete(`${url}/${id}`);
    if (response) {
      return response.data;
    }
  } catch (error) {
    return error;
  }
}

}
export default ApiService;