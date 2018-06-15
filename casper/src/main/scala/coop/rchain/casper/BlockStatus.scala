package coop.rchain.casper

sealed trait BlockStatus
sealed trait IncludeableBlock extends BlockStatus
sealed trait RejectableBlock  extends BlockStatus
sealed trait Slashable

case object Valid extends IncludeableBlock
// IncludeableEquivocation are blocks that would create an equivocation but are
// pulled in through a justification of another block
case object IncludeableEquivocation extends IncludeableBlock with Slashable
case object IgnorableEquivocation   extends RejectableBlock with Slashable
case object InvalidUnslashableBlock extends RejectableBlock
case object MissingBlocks           extends RejectableBlock

case object InvalidBlockNumber    extends RejectableBlock with Slashable
case object InvalidParents        extends RejectableBlock with Slashable
case object InvalidSequenceNumber extends RejectableBlock with Slashable
