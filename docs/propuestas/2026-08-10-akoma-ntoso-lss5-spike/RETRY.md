# Retry — spike AKN LSS:5

## Correcciones aplicadas

1. Expression IRI usa la versión consolidada del cuerpo `2026-01-15`; la reforma
   de la porción `2001-12-20` queda en `FRBRdate name=last-amendment-of-portion`.
2. Work conserva su autoridad; sólo Expression marca `FRBRauthoritative=false`.
   Manifestation no admite ese elemento en AKN 1.0; la desviación se documenta.
3. Manifestation añade `FRBRportion from=#art_5`.
4. `portion@includedIn=#lss` resuelve el `eId` de `original`, cuyo `href`
   identifica el Work contenedor; no se usa `activeRef`, pues la porción no lo modifica.
5. Se elimina `GUID`; `FRBRalias` conserva IDs internos.
6. `FRBRname=lss` coincide con el IRI; otro alias conserva `LSS`.
7. La inversa reconstruye el subconjunto interno, incluido `5.`; el arnés valida
   XSD y hash pinneado mediante `xmllint`.
8. Matriz R2 enumera todos los grupos de campos y el riesgo de versión.
9. La decisión dice "potencial" y declara que ningún consumidor fue probado.

La publicación, autor y versión del cuerpo se leen de `corpus/registry.yaml#LSS`;
la reforma de la disposición se lee de `LSS-005.json`. El arnés exige que la
versión estructurada coincida con `vigencia.nota_cuerpo` y con el XML generado.
