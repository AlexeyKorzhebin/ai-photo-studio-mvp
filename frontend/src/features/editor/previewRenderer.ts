import type { EditOperation } from '../../state/types'

export function buildPreviewStyle(operations: EditOperation[]): React.CSSProperties {
  let rotate = 0
  let scaleX = 1
  let scaleY = 1
  let brightness = 1
  let contrast = 1
  let saturation = 1
  let filterPreset = ''

  for (const operation of operations) {
    if (operation.kind === 'rotate') rotate += Number(operation.params.degrees ?? 0)
    if (operation.kind === 'flip') {
      if (operation.params.axis === 'horizontal') scaleX *= -1
      if (operation.params.axis === 'vertical') scaleY *= -1
    }
    if (operation.kind === 'tonal') {
      brightness *= Number(operation.params.brightness ?? 1)
      contrast *= Number(operation.params.contrast ?? 1)
      saturation *= Number(operation.params.saturation ?? 1)
    }
    if (operation.kind === 'filter') filterPreset = String(operation.params.preset ?? '')
  }

  const filters = [`brightness(${brightness})`, `contrast(${contrast})`, `saturate(${saturation})`]
  if (filterPreset === 'grayscale') filters.push('grayscale(1)')
  if (filterPreset === 'sepia') filters.push('sepia(0.8)')

  return {
    transform: `rotate(${rotate}deg) scale(${scaleX}, ${scaleY})`,
    filter: filters.join(' '),
    transition: 'transform 180ms ease, filter 180ms ease',
  }
}
