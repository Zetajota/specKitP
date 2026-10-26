# Reglas para agentes de IA en este repositorio

## Alcance y calidad

- Respetar `.specify/memory/constitution.md` y redactar en español los
  documentos y mensajes visibles para el estudiante.
- Escribir y ejecutar pruebas automatizadas para cualquier funcionalidad
  antes de marcar su tarea como terminada.
- No añadir cuentas, servicios de fondo, Docker ni otros componentes
  fuera del alcance de las especificaciones activas.

## Revisión obligatoria antes de cada push

1. Confirmar la rama actual, el remoto de destino y que el árbol de trabajo
   está limpio. No publicar bases de datos, entornos virtuales ni secretos.
2. Ejecutar `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verificar-antes-de-push.ps1`.
   El script consulta el remoto y compara la rama local con su contraparte
   remota o con `origin/main` si aún no existe una rama remota.
3. Si el remoto tiene commits que faltan localmente, integrar primero esos
   cambios con Git. En `main`, usar avance rápido cuando sea posible;
   si hay divergencia, hacer un merge explícito. En ramas de trabajo,
   integrar también `origin/main` antes de abrir o actualizar una solicitud
   de cambios.
4. Si aparece un conflicto, revisar cada archivo y conservar los cambios
   que cumplen la especificación. No elegir automáticamente «ours» o
   «theirs». Buscar marcadores de conflicto, ejecutar `git diff --check`,
   repetir las pruebas pertinentes y terminar el commit de integración.
5. Ejecutar de nuevo el script de comparación. Solo hacer `git push`
   cuando informe que la rama está lista. Si el push es rechazado porque
   el remoto avanzó, repetir desde el paso 2.
6. No usar `--force`, `--force-with-lease`, `reset --hard` ni sobrescribir
   trabajo remoto sin autorización explícita. Si no se puede integrar con
   seguridad o faltan credenciales, explicar el bloqueo y detener el push.

Esta regla evita publicar sobre un remoto desactualizado; la verificación
y la resolución de conflictos deben repetirse ante cambios concurrentes.
