import type { Profesor } from './Profesor';
import type { Categoria } from './Categoria';

export interface Socio {
  id: number;
  nombre: string;
  apellido: string;
  dni: string;
  email: string;
  telefono: string;
  fecha_inscripcion: string;
  profesor: Profesor;
  categorias: Categoria[];
}
