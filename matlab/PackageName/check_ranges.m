function result = check_ranges(data, column, min_val, max_val)
    % check_ranges - Check if all values are within a range.
    %
    % Args:
    %   data: Numeric array or struct array.
    %   column: Field name (for struct data) or empty (for numeric data).
    %   min_val: Minimum expected value.
    %   max_val: Maximum expected value.
    %
    % Returns:
    %   true if all non-NaN values are within [min_val, max_val].

    if isempty(data)
        result = true;
        return;
    end

    if isstruct(data)
        values = [data.(column)];
    else
        values = data(:)';
    end

    values = values(~isnan(values));

    if isempty(values)
        result = true;
    else
        result = all(values >= min_val) && all(values <= max_val);
    end
end
