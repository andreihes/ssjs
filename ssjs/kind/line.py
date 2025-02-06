import re
import typing
import ssjs.core.depo as depo
import ssjs.core.flex as flex
import ssjs.core.kind as kind


@depo.Depo.name('line')
class Line(kind.Kind):
    def make(self, args: flex.Flex) -> None:
        self.min = args.get('min', int)
        self.max = args.get('max', int)
        self.rep = args.get('re+', re.Pattern)
        self.ren = args.get('re-', re.Pattern)

    def scan(self, data: str) -> typing.Iterator[str]:
        if self.min is not None and len(data) < self.min:
            yield f'len < min: {len(data)} < {self.min}'

        if self.max is not None and len(data) > self.max:
            yield f'len > max: {len(data)} > {self.max}'

        if self.rep is not None and not self.rep.match(data):
            yield f'data !~ re+: data !~ "{self.rep}"'

        if self.ren is not None and self.ren.match(data):
            yield f'data =~ re-: data =~ "{self.ren}"'
